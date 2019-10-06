import time
import scrapy
from scrapy import Item
from scrapy.loader import ItemLoader
from gql import gql

from event_processor.util.data_utils import DataUtils
from event_processor.base.custom_spiders import ApiSpider
from event_processor.graphql_definitions.honeycomb import definition

class Honeycomb(ApiSpider):
    """Crawler for the API on the Honeycomb project website."""
    name = 'honeycomb'

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'The Honeycomb Project', 'https://events.thehoneycombproject.org/', date_format = '%a %b %d %Y %H:%M:%S', **kwargs)
        self.gql_url = 'https://the-honeycomb-project-api.herokuapp.com/gql'

    def parse(self, response):
        return self.get_events()

    def get_events(self):
        response = self.get_response_graphql(url=self.gql_url, gql_query=definition, params={'search': {'published': True, 'view': 'grid'}})

        # Don't show full events (open seats == 0)
        for docs in (docs for docs in response['events']['docs'] if docs['open'] > 0):
            program = docs['program']
            yield {
                'title': docs['name'],
                'description': program['description'],
                'address': f'{program["addressLineTwo"]} {program["city"]}, {program["state"]} {program["postal"]}',
                'event_time': {
                    'date': docs['date'].replace('GMT+0000 (Coordinated Universal Time)', ''),
                    'start_time': docs['startTime'],
                    'end_time': docs['endTime']
                },
                'url': f'{self.base_url}event/{docs["id"]}'
            }
