import time
from scrapy import Item
from scrapy.loader import ItemLoader
from categories import Category
from data_utils import DataUtils
from custom_spiders import ApiSpider
import scrapy
from gql import gql

class Honeycomb(ApiSpider):
    name = 'honeycomb'

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'The Honeycomb Project', 'https://events.thehoneycombproject.org/', date_format = '%Y-%m-%d', **kwargs)
    
    def parse(self, response):
        return self.get_events()
    
    def get_events(self):
        query = gql('''
            query EVENTS($search: EventSearchInput) {
                events(search: $search) {
                    docs {
                        id
                        name
                        date
                        startTime
                        endTime
                        shortDescription
                        description
                        favorite
                        open
                        openDate
                        closeDate
                        category {
                            id
                            name
                            photo
                            __typename
                        }
                        program {
                            id
                            shortDescription
                            cardImage
                            description
                            addressLineOne
                            addressLineTwo
                            headerImage
                            city
                            state
                            postal
                            takeNote
                            __typename
                        }
                        registrationOpensOn
                        hasCapacity
                        __typename
                    }
                    __typename
                }
            }
        ''')
        response = self.get_response_graphql(url='https://the-honeycomb-project-api.herokuapp.com/gql', gql_query=query, params={'search': {'published': True, 'view': 'grid'}})

        for docs in response['events']['docs']:
            program = docs['program']
            yield {
                'title': docs['name'],
                'description': program['shortDescription'] + program['description'],
                'address': f'{program["addressLineTwo"]} {program["city"]}, {program["state"]} {program["postal"]}',
                'event_time': {
                    'date': docs['date'],
                    'start_time': docs['startTime'],
                    'end_time': docs['endTime']
                },
                'url': f'{self.base_url}event/{docs["id"]}'
            }