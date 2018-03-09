from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import requests
import os
import json
import time

import sys
import os
sys.path.append(os.path.abspath('.'))
from event import Event
from categories import Category

def main():
    library_events = LibraryEvents()
    events = library_events.get_events('2018-03-10', '2018-03-12')
    lines = []

    # Add column headers
    lines.append(events[0].props_to_csv())
    # Add event data
    lines.extend([event.vals_to_csv() for event in events])
    write_to_file('events.csv', lines)
        

class LibraryEvents:
    def __init__(self):
        self.base_url = 'https://chipublib.bibliocommons.com/'

        self.date_format = '%m-%d-%Y'
        self.time_format = '%H:%M'

        self.MAX_ROWS = 50

        self.session = requests.Session()
        # Request headers to send
        self.session.headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        })
    
    def get_response(self, url, request_params):
        return self.session.get(self.base_url + url, params = request_params)

    def parse_response_json(self, response):
        loads = json.loads(response.content)
        # Don't return an array if it only contains one element
        return loads if (len(loads) != 1) else loads[0]
        
    def get_response_json(self, url, request_params, property_to_return = None):
        response = self.get_response(url, request_params)
        response_json = self.parse_response_json(response)
        return response_json if property_to_return == None else response_json[property_to_return]

    def get_next_events_json(self, start, start_date, end_date):
        request_params = {
            'client_scope': 'events', 
            'query': 'start={0}&rows={1}'.format(start, self.MAX_ROWS), 
            'facet_fields': 'branch_location_id', 
            'local_start': '{0} TO {1}'.format(start_date, end_date),
            'include_near_location': 'false'
        }
        return self.get_response_json('events/events/search', request_params, property_to_return = 'events')

    def get_events_json(self, start_date, end_date):
        start = 0
        events_json = []
        more_data = True

        while more_data:
            # Sleep to avoid overloading the server
            time.sleep(0.1)
            next_events_json = self.get_next_events_json(start, start_date, end_date)
            num_results = len(next_events_json)
            events_json.extend(next_events_json)
            # Keep querying until no more data is returned
            more_data = num_results > 0
            if (more_data):
                print('got events', start, 'to', start + num_results)
                # Events are returned in fixed increments
                start += num_results
        
        return events_json

    def get_locations_json(self, location_category):
        # location_category = 'locations' for branch locations and 'places' for non-branch locations
        request_params = {
            'client_scope': 'events', 
            'limit': '0'
        }
        return self.get_response_json('events/' + location_category, request_params, property_to_return = location_category)
    
    def get_branch_locations_json(self):
        return self.get_locations_json('locations')

    def get_nonbranch_locations_json(self):
        return self.get_locations_json('places')
    
    def get_locations_list(self, get_locations_func):
        return { location['id']: location['address'] for location in get_locations_func() }

    def get_branch_locations_list(self):
        return self.get_locations_list(self.get_branch_locations_json)

    def get_nonbranch_locations_list(self):
        return self.get_locations_list(self.get_nonbranch_locations_json)

    def convert_datetime_format(self, datetime_string, new_format):
        return parse(datetime_string).strftime(new_format)

    def get_time(self, datetime_string):
        return self.convert_datetime_format(datetime_string, self.time_format)
    
    def get_date(self, datetime_string):
        return self.convert_datetime_format(datetime_string, self.date_format)

    def get_address_string(self, location):
        # Any data that isn't included will be set to 'None', so just replace it with an empty string
        return ('{0} {1} {2}, {3} {4}'.format(
            location['number'], 
            location['street'], 
            location['city'], 
            location['state'], 
            location['zip'])).replace('None', '')

    def remove_html_tags(self, html_data):
        return BeautifulSoup(html_data, 'lxml').extract().text

    def get_events(self, start_date, end_date):
        events_json = self.get_events_json(start_date, end_date)
        branch_locations = self.get_branch_locations_list()
        nonbranch_locations = self.get_nonbranch_locations_list()

        events = []
        for event in events_json:
            details = event['definition']
            branch_location_id = details['branch_location_id']
            # Determine if branch or non-branch event
            if branch_location_id == None:
                non_branch_location_id = details['non_branch_location_id']
                location = nonbranch_locations[non_branch_location_id]
            else:
                location = branch_locations[branch_location_id]

            start_time = self.get_time(details['start'])
            end_time = self.get_time(details['end'])
            # Assume event is all day if no time is supplied
            if start_time == end_time == '00:00':
                start_time = end_time = 'All Day'

            # Don't show cancelled or full events
            if details['is_cancelled'] == True or event['is_full'] == True:
                continue

            events.append(Event(
                organization = 'Chicago Public Library',
                title = details['title'],
                description = self.remove_html_tags(details['description']),
                address = self.get_address_string(location),
                date = self.get_date(details['start']),
                start_time = start_time,
                end_time = end_time,
                url = ('{0}events/{1}').format(self.base_url, event['id']),
                price = 0.0,
                category = Category.LIBRARY
            ))

        return events


def pretty_json(json_data):
    return json.dumps(json_data, indent = 4)

def print_json(json_data):
    print(pretty_json(json_data)) 

def pretty_html(html_data):
    return BeautifulSoup(html_data, 'lxml').prettify()

def print_html(html_data):
    print(pretty_html(html_data))

def write_to_file(filename, data):
    if (os.path.isfile(filename)):
        os.remove(filename)

    with open(filename, 'w', encoding = 'utf-8') as f:
        f.writelines(data)    


if __name__ == '__main__':
    main()