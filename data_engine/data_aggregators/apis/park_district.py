import time
from event import Event
from categories import Category
from api_base import ApiBase
from data_utils import DataUtils


class ParkDistrict(ApiBase):
    # This is the max amount of rows that the API can return at one time
    MAX_ROWS = 50

    def __init__(self, start_date, end_date):
        super().__init__(' https://www.chicagoparkdistrict.com/',
                         start_date, end_date, date_format='%Y-%m-%d')

    def get_events(self):
        events = []
        events_response=self.post_response_json('cpd_maps/load_content', {'type': 'event'})
        for event in events_response:
            events.append(Event.from_dict({
                'organization': 'Chicago Park District',
                'title': event['title'],
                'address': event['location'],
                'url': f'{self.base_url}/{event["url"]}'
            }, self.time_utils.date_format))
        self.save_events(events)
    # append each new event to a list
    # events = [] #create an empty list
    # events.append({
    #     'organization': 'Chicago Park District'
    #     'title': 
    #     'description':
    #     'address': 
    #     'date':
    #     'start_time':
    #     'end_time':
    #     'url_for':
    #     'price':
    #     'category':


