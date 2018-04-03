import scrapy
from urllib import parse
from collections import namedtuple
from aggregator_base import AggregatorBase
from event import Event

class SpiderBase(AggregatorBase):
    # This class includes all functionality that should be shared by spiders

    KeyValuePair = namedtuple('KeyValuePair', ['key', 'value'])
    
    def get_request(self, url, request_params):
        return scrapy.Request(f'{self.base_url}{url}?{parse.urlencode(request_params)}')

    # Sometimes it's easier to remove html tags with lxml than with Scrapy's selectors
    def xpath_remove_html(self, name, response, path, remove_all = False):
        xpath_result = self.xpath_extract(name, response, path)
        return self.KeyValuePair(name, self.remove_html(xpath_result.value, remove_all))
    
    def css_remove_html(self, name, response, path, remove_all = False):
        css_result = self.css_extract(name, response, path)
        return self.KeyValuePair(name, self.remove_html(css_result.value, remove_all))

    def xpath_extract(self, name, response, path):
        return self.KeyValuePair(name, response.selector.xpath(path).extract())

    def css_extract(self, name, response, path):
        return self.KeyValuePair(name, response.css(path).extract())

    def create_events(self, *args):
        count = len(args[0].value)
        for arg in args:
            if len(arg.value) != count:
                raise ValueError("Selectors returned data of differing lengths")

        return [Event.from_dict({arg.key: arg.value[i] for arg in args}) for i in range(count)]
            

