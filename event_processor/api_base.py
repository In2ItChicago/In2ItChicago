import requests
import json
import time

from aggregator_base import AggregatorBase
from cache_call import cache_call
from config import config


class ApiBase(AggregatorBase):
    # Placeholder values that can be used if no request needs to be made through Scrapy
    allowed_domains = ['wikipedia.org','en.wikipedia.org']
    start_urls = ['https://www.wikipedia.org/']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = requests.Session()
        # Request headers to send
        self.session.headers.update({
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
    def get_response(self, url = '', request_params=None, headers=None):
        response = self.session.get(self.base_url + url, params = request_params, headers = headers)
        if not response.ok:
            raise ValueError(response.text)
        return response

    def parse_response_json(self, response):
        loads = json.loads(response.content)
        # Don't return an array if it only contains one element
        return loads if (len(loads) != 1) else loads[0]
        
    def get_response_json(self, url, request_params, property_to_return=None):
        response = self.get_response(url, request_params=request_params, headers={'Accept': 'application/json, text/javascript, */*; q=0.01'})
        if not response.ok:
            raise ValueError(response.text)
        response_json = self.parse_response_json(response)
        return response_json if property_to_return == None else response_json[property_to_return]

    def get_events(self):
        # Override me
        pass