import scrapy
from urllib import parse

class SpiderBase(object):
    # This class includes all functionality that should be shared by spiders
    def __init__(self, base_url, start_date, end_date):
        self.base_url = base_url
        self.start_date = start_date
        self.end_date = end_date
    
    def get_request(self, url, request_params):
        return scrapy.Request('{0}{1}?{2}'.format(self.base_url, url, parse.urlencode(request_params)))
