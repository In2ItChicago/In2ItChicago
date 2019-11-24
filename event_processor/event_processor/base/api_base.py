import json
import time

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from event_processor.base.aggregator_base import AggregatorBase
from event_processor.util.cache_call import cache_call
from event_processor.util.http_utils import HttpUtils
from event_processor.config import config


class ApiBase(AggregatorBase):
    # Placeholder values that can be used if no request needs to be made through Scrapy
    allowed_domains = ['wikipedia.org','en.wikipedia.org']
    start_urls = ['https://www.wikipedia.org/']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = HttpUtils.get_session({
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        })

    def wait(self, sleep_time=None):
        if sleep_time == None:
            time.sleep(config.api_delay_seconds)
        else:
            time.sleep(sleep_time)

    @cache_call
    def get_response(self, url=None, endpoint='', request_params=None, headers=None):
        if url == None:
            url = self.base_url + endpoint
        response = self.session.get(url, params = request_params, headers = headers)
        if not response.ok:
            raise ValueError(response.text)
        return response

    def parse_response_json(self, response):
        loads = json.loads(response.content)
        # Don't return an array if it only contains one element
        return loads if (len(loads) != 1) else loads[0]
        
    def get_response_json(self, url=None, endpoint='', request_params=None, property_to_return=None):
        response = self.get_response(url, endpoint, request_params, {'Accept': 'application/json, text/javascript, */*; q=0.01'})
        if not response.ok:
            raise ValueError(response.text)
        response_json = self.parse_response_json(response)
        return response_json if property_to_return == None else response_json[property_to_return]

    @cache_call
    def get_response_graphql(self, url=None, endpoint='', gql_query=None, params=None):
        if url == None:
            url = self.base_url + endpoint
        transport = RequestsHTTPTransport(url=url, use_json=True)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        return client.execute(gql_query, params)

    def get_events(self):
        # Override me
        pass