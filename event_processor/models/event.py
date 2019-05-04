import scrapy
import re
import usaddress
from util.time_utils import TimeUtils
from util.data_utils import DataUtils
from scrapy.loader.processors import MapCompose, Compose, Join, TakeFirst
from scrapy.loader import ItemLoader

def custom_field():
    return scrapy.Field(input_processor=MapCompose(DataUtils.remove_html), output_processor=Join())

def price_field():
    return scrapy.Field(input_processor=MapCompose(
            lambda value: value.replace('$', '') if type(value) == str else value, 
            DataUtils.remove_html, float), 
        output_processor=TakeFirst())

def url_field():
    return scrapy.Field(input_processor=MapCompose(DataUtils.remove_html, lambda value: value.rstrip('//')), 
    output_processor=Join())

def category_field():
    return scrapy.Field(input_processor=MapCompose(lambda value: value.name), output_processor=Join())

def address_field():
    def parse_address(value):
        parsed = usaddress.parse(value)
        contains_field = lambda field: any(address_part[1] == field for address_part in parsed)
        default_field = lambda field, default: f' {default}' if not contains_field(field) else ''
        return f'{value}{default_field("PlaceName", "Chicago")}{default_field("StateName", "IL")}'
        
    return scrapy.Field(input_processor=MapCompose(
            DataUtils.remove_html,
            parse_address),
        output_processor=Join())

def date_field():
    def parse_date(value):
        date_format = value['date_format']
        time_utils = TimeUtils(date_format=date_format)
        date_obj = {**create_time_data(), **value}
        start_timestamp, end_timestamp = time_utils.get_timestamps(date_obj)
        return {
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp
        }

    return scrapy.Field(input_processor=MapCompose(DataUtils.remove_html, parse_date), output_processor=TakeFirst())

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

class Event(scrapy.Item):
    organization = custom_field()
    title = custom_field()
    description = custom_field()
    address = address_field()
    url = url_field()
    price = price_field()
    category = category_field()
    event_time = date_field()
    geocode_id = scrapy.Field()

class EventLoader():
    def __init__(self, *args, **kwargs):
        item_loader = ItemLoader(item=Event())
        for key, value in kwargs.items():
            try:
                item_loader.add_value(key, value)
            except KeyError:
                raise KeyError(f'{key} is not a valid event field')
        self.item = item_loader.load_item()

class EventManager:
    def __init__(self):
        self.events = {}
    
    def update(self, key, event):
        # Add properties to the event if it has been created already, else create a new event
        if key in self.events:
            self.events[key].update(event)
        else:
            self.events[key] = event
    
    def to_dicts(self):
        return [dict(event) for event in list(self.events.values())]