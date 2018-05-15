# -*- coding: utf-8 -*-
import scrapy
#from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from event import Event
from categories import Category
from spider_base import SpiderBase

class LWVchicago(Spider, SpiderBase):
    name = 'lwvchicago'
    allowed_domains = ['lwvchicago.org']

    # My understanding is that the rule sets parameters for crawling, 
    # since this site uses a static table for events, no rule is needed

    def __init__(self, start_date, end_date):
        SpiderBase.__init__(self, 'http://lwvchicago.org/', start_date, 
        	end_date, date_format = '%W, %M %e, %Y')

    def start_requests(self):
        yield self.get_request('calendar.html', {})

    def parse(self, response):
        titles = self.extract('title', response.css, 'td span::text')
        times = self.re_extract('time_range', response.css, "[scope='row']::text", r'^\n(.+)')
        dates = self.re_extract('date', response.css, "[scope='row']::text", r'^[A-Z].+')

        # Correct text plus leading newline, is missing one element that doesn't have a description
        descriptions = self.extract('description', response.xpath, '//td[span]/text()[starts-with(., "\n")][normalize-space()]')
        
        # Need to figure out how to extract text in a block, not breaking on newlines
        addresses = self.extract('address', response.xpath, '//td[@scope]/following-sibling::*[name() = "td" and (position() = 1)]').remove_html()

        return self.create_events('League of Women Voters of Chicago', titles, times, dates, addresses, descriptions)