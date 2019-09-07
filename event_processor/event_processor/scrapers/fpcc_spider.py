# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from event_processor.base.custom_spiders import ScraperSpider
from scrapy.linkextractors import LinkExtractor

from event_processor.models.category import Category
from event_processor.util.data_utils import DataUtils
from pprint import pprint

def return_first_or_empty(arr):
    print("********************************************************* PARSING ")
    if (not arr is None) and (len(arr) > 0):
        print("Returning: " + (str(arr[0])))
        return [ str(arr[0]) ] 
    return ""

class FpccSpider(ScraperSpider):
    """
    Forest Preserves of Cook County

    maybe take advantage of their API that returns HTML data??
    https://ec.samaritan.com/recruiter/fastbackend.php?dnc=547&rCalendar_act=getTabContent&key=RecruiterCalendar_recruiter504&date=2019-08-10&id=180540&childs=3809305
    """
    name = 'fpcc'
    allowed_domains = ['ec.samaritan.com']
 
    def __init__(self, name=None, **kwargs):
        self.recruiterID = 1405 # not sure what this is or if it needs to vary?
        super().__init__(self, 'Forest Preserves of Cook County', 'https://ec.samaritan.com/', date_format='%m/%d/%y', **kwargs)

    def start_requests(self):
        print("start requests...")
        #yield self.get_request('recruiter/index.php?class=RecruiterCalendar&recruiterID=' + str(self.recruiterID), {})
        yield self.get_request('recruiter/index.php?class=OppSearch&recruiterID=' + str(self.recruiterID) + '&act=search_all&type=all', {})

    def parse(self, response):  
        print("Parsing page...") 
        #for result in response.css("div.result-record"): 
        #    print("result...")
        #   print(result)
        return  { 
            'title': return_first_or_empty(response.css('a#view_details_link::text').extract()),
            'url': return_first_or_empty(response.css('a#view_details_link::attr(href)').extract()),
            'event_time': self.create_time_data(
                time=["1:00pm"],
                date=["9/3/19"]),
                'address': ["address"],
            'description': ["description"]
        }
    