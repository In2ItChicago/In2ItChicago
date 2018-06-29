import time
from event import Event
from categories import Category
from api_base import ApiBase
from data_utils import DataUtils

class LibraryEvents(ApiBase):
    # This is the max amount of rows that the API can return at one time
    MAX_ROWS = 50

    def __init__(self, start_date, end_date):
        super().__init__('https://chipublib.bibliocommons.com/', start_date, end_date, date_format = '%Y-%m-%d')

    def get_next_events_json(self, start):
        request_params = {
            'client_scope': 'events', 
            'query': f'start={start}&rows={self.MAX_ROWS}',
            'facet_fields': 'branch_location_id', 
            'local_start': f'{self.start_date} TO {self.end_date}',
            'include_near_location': 'false'
        }
        return self.get_response_json('events/events/search', request_params, property_to_return = 'events')

    def get_events_json(self):
        start = 0
        events_json = []
        more_data = True

        while more_data:
            # Sleep to avoid overloading the server
            time.sleep(0.1)
            next_events_json = self.get_next_events_json(start)
            num_results = len(next_events_json)
            events_json.extend(next_events_json)
            # Keep querying until no more data is returned
            more_data = num_results > 0
            if (more_data):
                #print('got events', start, 'to', start + num_results)
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

    def get_address_string(self, location):
        # Any data that isn't included will be set to 'None', so just replace it with an empty string
        return f"{location['number']} {location['street']} {location['city']}, {location['state']} {location['zip']}".replace('None', '')

    def get_events(self):
        events_json = self.get_events_json()
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

            try:
                date, start_time = details['start'].split('T')
                end_time = details['end'].split('T')[1]
            except ValueError:
                # Assume event is all day if no time is supplied
                date = details['start']
                start_time = end_time = 'All Day'

            # Don't show cancelled or full events
            if details['is_cancelled'] == True or event['is_full'] == True:
                continue

            events.append(Event.from_dict({
                'organization': 'Chicago Public Library',
                'title': details['title'],
                'description': DataUtils.remove_html(details['description']),
                'address': self.get_address_string(location),
                'date': date,
                'start_time': start_time,
                'end_time': end_time,
                'url': f'{self.base_url}/{event["id"]}',
                'price': 0.0,
                'category': Category.LIBRARY
            }, self.time_utils.date_format))
        self.save_events(events)