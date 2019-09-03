# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from base.custom_spiders import ScraperSpider
from scrapy.linkextractors import LinkExtractor

from models.category import Category
from util.data_utils import DataUtils
from pprint import pprint

def return_first_or_empty(arr):
    print("********************************************************* PARSING ")
    print(arr) 
    print(str(len(arr)))
    if (not arr is None) and (len(arr) > 0):
        print("Returning: " + (str(arr[0])))
        return str(arr[0]) 
    return ""

# Forest Preserves of Cook County

# maybe take advantage of their API that returns HTML data??
# https://ec.samaritan.com/recruiter/fastbackend.php?dnc=547&rCalendar_act=getTabContent&key=RecruiterCalendar_recruiter504&date=2019-08-10&id=180540&childs=3809305

class FpccSpider(ScraperSpider):
    name = 'fpcc'
    allowed_domains = ['ec.samaritan.com']
 
    def __init__(self, name=None, **kwargs):
        self.recruiterID = 1405 # not sure what this is or if it needs to vary?
        super().__init__(self, 'Forest Preserves of Cook County', 'https://ec.samaritan.com/', date_format='%Y', **kwargs)

    def start_requests(self):
        print("start requests...")
        yield self.get_request('recruiter/index.php?class=RecruiterCalendar&recruiterID=' + str(self.recruiterID), {})
        #yield self.get_request('recruiter/index.php?class=OppSearch&recruiterID=' + str(self.recruiterID) + '&act=search_all&type=all', {})

    def parse(self, response):  
        print("Parsing page...") 
        for result in response.css("div.result-record"): 
            print("result...")
            print(result)
            yield  { 
                'title': return_first_or_empty(result.css('a#view_details_link::text').extract()),
                'url': return_first_or_empty(result.css('a#view_details_link::attr(href)').extract()),
                'event_time': {'date': "date", 
                    'time_range': "range"},
                'address': "address",
                'description': "description"
            }
    