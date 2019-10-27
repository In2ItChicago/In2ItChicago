import json
import time

from event_processor.base.aggregator_base import AggregatorBase
from event_processor.config import config

from scrapy_splash import SplashRequest

class SplashBase(AggregatorBase):
    """Base class for spiders that use splash for retrieving data generated through dynamic javascript content"""
    # Placeholder values that can be used if no request needs to be made through Scrapy

    # maybe define some template lua or javascript scripts for common scraping tasks??
    #   https://splash.readthedocs.io/en/stable/api.html#execute-javascript
    # mabybe a script template for "click on element" ??

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):
        """Start the request as a splash request"""
        print("Start requests")
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        for q in response.css("div.quote"):
            quote = QuoteItem()
            quote["author"] = q.css(".author::text").extract_first()
            quote["quote"] = q.css(".text::text").extract_first()
            yield quote