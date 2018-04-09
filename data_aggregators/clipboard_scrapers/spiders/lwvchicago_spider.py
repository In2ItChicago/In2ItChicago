# -*- coding: utf-8 -*-
import scrapy
#from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from event import Event
from categories import Category
from spider_base import SpiderBase

class LWVchicago(SpiderBase):
    name = 'lwvchicago'
    allowed_domains = ['http://lwvchicago.org/']

    # My understanding is that the rule sets parameters for crawling, 
    # since this site uses a static table for events, no rule is needed

    def __init__(self, start_date, end_date):
        SpiderBase.__init__(self, 'http://lwvchicago.org/', start_date, 
        	end_date, date_format = '%W, %M %e, %Y')

    def start_requests(self):
        yield self.get_request('calendar.html')

    # can this live in SpiderBase?
    def css_re_extract(self, name, response, path, pattern):
        return self.KeyValuePair(name, response.css(path).re(pattern))

    def parse_link(self):
    	titles = self.css_extract('title', response, 'td span::text')
        times = self.css_re_extract('time_range', response, "[scope='row']::text", r'^\n(.+)')
        dates = self.css_re_extract('date', response, "[scope='row']::text", r'^[A-Z].+')

        # Correct text plus leading newline, is missing one element that doesn't have a description
        descriptions = self.xpath_extract('description', response, '//td[span]/text()[starts-with(., "\n")][normalize-space()]')
        
        # Need to figure out how to extract text in a block, not breaking on newlines
        addresses = self.xpath_extract('address', response, '//td[@scope]/following-sibling::*[name() = "td" and (position() = 1)]')

        for event in self.create_events(titles, times, dates, addresses, descriptions):
            if self.time_utils.day_is_between(event['date'], self.start_date, self.end_date):
                event['organization'] = 'League of Women Voters of Chicago'
                yield event