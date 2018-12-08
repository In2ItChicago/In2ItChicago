import os
import json
import re
from time_utils import TimeUtils
from multiprocessing import Lock
from config import config
from event_hashes import EventHashes
import requests

class AggregatorBase:
    # This class includes functionality that should be shared by spiders and API-based classes

    def __init__(self, base_url, start_date, end_date, date_format, request_date_format = None):
        # date_format is the string that specifies the date style of the target website
        if request_date_format == None:
            request_date_format = date_format

        self.time_utils = TimeUtils(date_format)
        self.base_url = base_url
        self.identifier = re.sub(r'\W', '', base_url)
        self.update_mutex = Lock()
        
        request_format_utils = TimeUtils('%m-%d-%Y')
        self.start_date = request_format_utils.convert_date_format(start_date, request_date_format)
        self.end_date = request_format_utils.convert_date_format(end_date, request_date_format)
        self.start_timestamp = request_format_utils.min_timestamp_for_day(start_date)
        self.end_timestamp = request_format_utils.max_timestamp_for_day(end_date)

    def save_events(self, event_list):
        if len(event_list) == 0:
            return
        new_hash = EventHashes.create_hash(event_list)
        print(f'Found {len(event_list)} events for {event_list[0]["organization"]}.')
        if new_hash == EventHashes.get(self.identifier):
            print('Nothing to update.')
            return
        EventHashes.set(self.identifier, new_hash)

        with self.update_mutex:
            response = requests.post(config.db_put_events, json=event_list)
        if not response.ok:
            raise ValueError(response.text)
        else:
            print(f'Saved {len(event_list)} events for {event_list[0]["organization"]}')