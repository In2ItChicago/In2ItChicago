import scrapy
from urllib import parse
from aggregator_base import AggregatorBase

class SpiderBase(AggregatorBase):
    # This class includes all functionality that should be shared by spiders

    def xpath_func(self, data):
        return data.xpath

    def css_func(self, data):
        return data.css
    
    def get_request(self, url, request_params={}):
        return scrapy.Request(f'{self.base_url}{url}?{parse.urlencode(request_params)}')

    def extract_multiple(self, name_funcs, extracted_data):
        return_data = dict()
        for name, name_func in name_funcs.values():
            return_data[name] = [name_func(data) for data in extracted_data]
        return return_data

    def empty_check_extract(self, base_selector, extractor, path, default_value=''):
        return list(map(lambda data: default_value if len(data) == 0 else data[0], [extractor(base_data)(path).extract() for base_data in base_selector]))

    def create_time_data(self, **kwargs):
        count = len(list(kwargs.values())[0])
        for value in kwargs.values():
            if len(value) != count:
                raise ValueError(f'{self.organization}: Time selectors returned data of differing lengths')
        return [{key: value[i] for key, value in kwargs.items()} for i in range(count)]
        