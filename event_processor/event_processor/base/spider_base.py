import scrapy
from urllib import parse
from event_processor.base.aggregator_base import AggregatorBase

class SpiderBase(AggregatorBase):
    # This class includes all functionality that should be shared by spiders

    def xpath_func(self, data):
        return data.xpath

    def css_func(self, data):
        return data.css
    
    def get_request(self, url, request_params={}):
        """Call a scrapy request with the given url using the given parameters"""
        return scrapy.Request(f'{self.base_url}{url}?{parse.urlencode(request_params)}')

    def extract_multiple(self, name_funcs, extracted_data):
        return_data = dict()
        for name, name_func in name_funcs.values():
            return_data[name] = [name_func(data) for data in extracted_data]
        return return_data

    def empty_check_extract(self, base_selector, extractor, path, default_value=''):
        """??? Convinience function for getting specific data out each result returned by a base selector. 
            - base_selector: The base selector for each element you want to get data from, such as '.item' or '.result'
            - extractor: The function that will be used to extract
            - path: An (xpath?) or (selector?) that is passed into the extractor function which retrieves each specific piece of data.
            - default_value: If no value is found in the given selector, it will default to this value.
                 If this is not specified, it will be an empty string.
        """
        return list( \
                map(lambda data: \
                        default_value if len(data) == 0 \
                        else data[0], \
                        [extractor(base_data)(path).extract() for base_data in base_selector]) \
                    )

    def create_time_data(self, **kwargs):
        count = len(list(kwargs.values())[0])
        for value in kwargs.values():
            if len(value) != count:
                raise ValueError(f'{self.organization}: Time selectors returned data of differing lengths')
        return [{key: value[i] for key, value in kwargs.items()} for i in range(count)]
        