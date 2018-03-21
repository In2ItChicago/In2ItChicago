import scrapy
import re
from time_utils import TimeUtils

class Event(scrapy.Item):
    date = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    time_range = scrapy.Field()
    organization = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()

    time_helper = TimeUtils(date_format = '%m-%d-%Y', time_format = '%H:%M')

    def get_item_with_default(self, key, default = ''):
        try:
            return super().__getitem__(key)
        except KeyError:
            return default

    def __setitem__(self, key, value):
        # Unfortunately, property decorators don't work with dictionary keys
        # Instead, intercept the __setitem__ call for certain properties and format them before saving
        scrapy_set_item = super().__setitem__
        if key == 'date':
            scrapy_set_item(key, self.time_helper.get_date(value))

        # time_range = start_time - end_time
        # Whenever one property changes, also update the other one(s)
        elif key in ('start_time', 'end_time'):
            scrapy_set_item(key, self.time_helper.get_time(value))
            start = self.get_item_with_default('start_time')
            end = self.get_item_with_default('end_time')
            scrapy_set_item('time_range', self.time_helper.format_start_end(start, end))

        elif key == 'time_range':
            start, end = self.time_helper.get_times(value)
            scrapy_set_item('start_time', start)
            scrapy_set_item('end_time', end)
            scrapy_set_item(key, self.time_helper.format_start_end(start, end))

        elif key == 'url':
            scrapy_set_item(key, value.strip().rstrip('//'))

        else:
            super().__setitem__(key, value)

    def update(self, event):
        for key, value in event.items():
            self[key] = value

    def props_to_csv(self):
        return ','.join(self.keys()) + '\n'

    def vals_to_csv(self):
        return ','.join('"{0}"'.format(str(self[key]).replace('"', '')) for key in self.keys()) + '\n'

class EventManager(object):
    def __init__(self):
        self.events = {}
    
    def update(self, key, event):
        # Add properties to the event if it has been created already, else create a new event
        if key in self.events:
            self.events[key].update(event)
        else:
            self.events[key] = event