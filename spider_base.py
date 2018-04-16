import scrapy
from urllib import parse
from aggregator_base import AggregatorBase
from event import Event, EventFieldData

class SpiderBase(AggregatorBase):
    # This class includes all functionality that should be shared by spiders

    def get_request(self, url, request_params):
        return scrapy.Request(f'{self.base_url}{url}?{parse.urlencode(request_params)}')

    def extract(self, name, extractor, path):
        # Remove leading and trailing whitespace from all extracted values
        return EventFieldData(name, list(map(lambda s: s.strip(), extractor(path).extract())))

    def re_extract(self, name, extractor, path, pattern):
        return EventFieldData(name, list(map(lambda s: s.strip(), extractor(path).re(pattern))))

    def extract_multiple(self, name_funcs, extractor, path):
        """
        This method is necessary when there are multiple fields contained within a single xpath selector (e.g. a date and a time).
        name_funcs should be a dictionary in which the keys are event property names and the values are functions that extract
        the value that matches that key.
        """
        for name in name_funcs.keys():
            yield EventFieldData(name, list(map(lambda s: name_funcs[name](s).strip(), extractor(path).extract())))
    
    def empty_check_extract(self, name, base_selector, extractor_name, path):
        """
        Search for all values that match the xpath selector within the base selector and add a default value if nothing is found.
        Scrapy's selectors don't add anything to the response array if no value is found, so this
        method is necessary for semi-structured html blocks where a field could be missing.
        """
        data = []
        for base_data in base_selector:
            extracted_data = eval(f'base_data.{extractor_name}(path).extract()')
            # Add a placeholder value if nothing was found on the site
            if len(extracted_data) == 0:
                extracted_data = ['']
            data.extend(extracted_data)
        
        return EventFieldData(name, data)

    def create_events(self, *args):
        count = len(args[0].data)
        for arg in args:
            if len(arg.data) != count:
                # All selectors must return the same amount of data because it's impossible to know which event is missing data otherwise
                raise ValueError('Selectors returned data of differing lengths')

        return [Event.from_dict(self.time_utils.old_date_format, {arg.item: arg.data[i] for arg in args}) for i in range(count)]
            

