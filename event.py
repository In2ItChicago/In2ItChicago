import scrapy
import re
from time_utils import TimeUtils
from data_utils import DataUtils

class Event(scrapy.Item):
    date = scrapy.Field()
    # setting start_time or end_time will also update time_range when __setitem__ is called and vice versa
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
    # start_date and end_date will automatically be updated based on whether date contains one or two dates
    date = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    is_multiple_days = scrapy.Field()
    time_helper = TimeUtils()

    def set_time_format(self, old_date_format):
        self.time_helper.old_date_format = old_date_format
        self.time_helper.new_date_format = '%m-%d-%Y'

    @classmethod
    def from_dict(cls, old_date_format, event_dict):
        event = cls()
        event.set_time_format(old_date_format)
        
        for key, value in event_dict.items():
            event[key] = value
        return event

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
            start, end = self.time_helper.get_dates(value)
            scrapy_set_item('is_multiple_days', end != None)
            scrapy_set_item('date', self.time_helper.format_start_end(start, end) if end != None else start)
            if end == None:
                end = start
            scrapy_set_item('start_date', start)
            scrapy_set_item('end_date', end)

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
            scrapy_set_item('time_range', self.time_helper.format_start_end(start, end))

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

class EventManager:
    def __init__(self):
        self.events = {}
    
    def update(self, key, event):
        # Add properties to the event if it has been created already, else create a new event
        if key in self.events:
            self.events[key].update(event)
        else:
            self.events[key] = event

class EventFieldData:
    def __init__(self, item, data):
        self.item = item
        self.data = data

    def remove_html(self, remove_all_whitespace = False):
        self.data = DataUtils.remove_html(self.data, remove_all_whitespace)
        return self
    
    def map(self, func):
        self.data = list(map(func, self.data))
        return self