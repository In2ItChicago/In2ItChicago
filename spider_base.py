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

    def extract(self, name, response, path, extractor):
        return self.KeyValuePair(name, extractor(path).extract())
    
    def empty_check_extract(self, name, base_selector, path, extractor):
        # Search for all values within the base selector and add a default value if nothing is found
        # Scrapy's selectors don't add anything to the response array if no value is found, so this
        # method is necessary for semi-structured html blocks where a field could be missing
        data = []
        for base_data in base_selector:
            extracted_data = extractor(base_data, path).extract()
            # Add a placeholder value if nothing was found on the site
            if len(extracted_data) == 0:
                extracted_data = ['']
            data.extend(extracted_data)
        
        return self.KeyValuePair(name, data)

    def xpath_empty_check_extract(self, name, base_selector, path):
        return self.empty_check_extract(name, base_selector, path, (lambda base_data, path: base_data.xpath(path)))
    
    def css_empty_check_extract(self, name, base_selector, path):
        return self.empty_check_extract(name, base_selector, path, (lambda base_data, path: base_data.css(path)))

    def xpath_extract(self, name, response, path):
        return self.extract(name, response, path, response.selector.xpath)

    def css_extract(self, name, response, path):
        return self.extract(name, response, path, response.css)

    def create_events(self, *args):
        count = len(args[0].value)
        for arg in args:
            if len(arg.value) != count:
                # All selectors must return the same amount of data because it's impossible to know which event is missing data otherwise
                raise ValueError('Selectors returned data of differing lengths')

        return [Event.from_dict({arg.key: arg.value[i] for arg in args}) for i in range(count)]
            

