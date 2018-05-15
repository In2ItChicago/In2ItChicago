import scrapy
import re
from time_utils import TimeUtils
from data_utils import DataUtils

class Event(scrapy.Item):
    start_timestamp = scrapy.Field()
    end_timestamp = scrapy.Field()
    organization = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()

    time_utils = TimeUtils()

    def set_time_format(self, date_format):
        self.time_utils.date_format = date_format

    @staticmethod
    def create_time_data():
        return {
            'time': None,
            'start_time': None,
            'end_time': None,
            'time_range': None,
            'date': None,
            'start_date': None,
            'end_date': None,
            'start_timestamp': None,
            'end_timestamp': None
        }

    @classmethod
    def from_dict(cls, event_dict, date_format=''):
        event = cls()
        event.set_time_format(date_format)

        time_data = Event.create_time_data()
        
        for key, value in event_dict.items():
            if key in time_data:
                time_data[key] = value
            else:
                event[key] = value
        event['time_data'] = time_data
        return event

    def to_dict(self):
        return { key: self[key] for key in self.keys() }

    def get_item_with_default(self, key, default = ''):
        try:
            return super().__getitem__(key)
        except KeyError:
            return default

    def __setitem__(self, key, value):
        # Unfortunately, property decorators don't work with dictionary keys
        # Instead, intercept the __setitem__ call for certain properties and format them before saving
        scrapy_set_item = super().__setitem__
        if key == 'time_data':
            start_timestamp, end_timestamp = self.time_utils.get_timestamps(value)
            scrapy_set_item('start_timestamp', start_timestamp)
            scrapy_set_item('end_timestamp', end_timestamp)

        elif key == 'url':
            scrapy_set_item(key, value.strip().rstrip('//'))

        elif key == 'category':
            # Can't serialze enums to json
            scrapy_set_item(key, value.name)

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