import scrapy
from urllib import parse
from aggregator_base import AggregatorBase

class SpiderBase(AggregatorBase):
    # This class includes all functionality that should be shared by spiders
    
    def get_request(self, url, request_params):
        return scrapy.Request('{0}{1}?{2}'.format(self.base_url, url, parse.urlencode(request_params)))

    # Sometimes it's easier to remove html tags with lxml than with Scrapy's selectors
    def xpath_remove_html(self, response, path):
        return self.remove_html(self.xpath_extract(response, path))
    
    def css_remove_html(self, response, path):
        return self.remove_html(self.css_extract(response, path))

    def xpath_extract(self, response, path):
        return response.selector.xpath(path).extract()

    def css_extract(self, response, path):
        return response.css(path).extract()
