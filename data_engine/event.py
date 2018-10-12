import scrapy
import re
from time_utils import TimeUtils
from data_utils import DataUtils

class Event(scrapy.Item):
    # When creating an event, use these values as keys
    # The exception to this is start_timestamp and end_timestamp
    # You can pass those in directly if the data is already formatted
    # as a Unix timestamp, otherwise, pass in the data as defined in the
    # create_time_data function below
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
        # When creating an event, you'll want to pass in the data that matches
        # how the data is formatted on the site you're pulling from
        return {
            # Use time if only one time is supplied for the event (not time range)
            'time': None,
            # Use start_time and end_time if the site supplies distinct data for these two values
            'start_time': None,
            'end_time': None,
            # Use time_range if the start and end time is supplied in a single string ex: 6:00-8:00 PM
            'time_range': None,
            # Use date if the event could be one or multiple days but it is contained in a single string
            # This is done this way because some sites have data that could be single days or multiple days
            'date': None,
            # Use start_date and end_date if the site supplies distinct data for these two values
            'start_date': None,
            'end_date': None,
            # Use start_timestamp and end_timestamp if the data is formatted like a Unix timestamp
            'start_timestamp': None,
            'end_timestamp': None
        }

    @classmethod
    def from_dict(cls, event_dict, date_format=''):
        event = cls()
        event.set_time_format(date_format)

        time_data = Event.create_time_data()
        time_data_set = False
        for key, value in event_dict.items():
            value = DataUtils.remove_html(value)
            if key in time_data:
                time_data[key] = value
                time_data_set = True
            else:
                event[key] = value
        if time_data_set:
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
            scrapy_set_item(key, value)

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

    def remove_html(self):
        self.data = DataUtils.remove_html(self.data)
        return self

    def remove_whitespace(self):
        self.data = DataUtils.remove_whitespace(self.data)
        return self
    
    def map(self, func):
        self.data = list(map(func, self.data))
        return self