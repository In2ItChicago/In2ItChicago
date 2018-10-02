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

    def __init__(self, start_date, end_date):
        SpiderBase.__init__(self, 'http://lwvchicago.org/', start_date, 
        	end_date, date_format = '%W, %M %e, %Y')

    def start_requests(self):
        yield self.get_request('calendar.html', {})

    def parse(self, response):
        base_selector = response.css('.bold.red')

        titles = self.extract('title', response.css, 'td span::text')
        times = self.re_extract('time_range', response.css, "[scope='row']::text", r'^\n(.+)')
        dates = self.re_extract('date', response.css, "[scope='row']::text", r'^[A-Z].+')

        # Correct text plus leading newline, is missing one element that doesn't have a description
        #descriptions = self.extract('description', response.xpath, '//td[span]/text()[starts-with(., "\n")][normalize-space()]')
        #descriptions = self.empty_check_extract('description', base_selector, 'xpath', '//td[span]/text()[starts-with(., "\n")][normalize-space()]')
        descriptions = self._parse_description(response)
        
        # Need to figure out how to extract text in a block, not breaking on newlines
        addresses = self.extract('address', response.xpath, '//td[@scope]/following-sibling::*[name() = "td" and (position() = 1)]').remove_html()


        return self.create_events('League of Women Voters of Chicago', titles, times, dates, addresses, descriptions)

        #Full name and description
        #self.response.xpath('//td[@scope]/following-sibling::*[name() = "td" and (position() = 2)]').extract()

    def _parse_description(self, response):
        all_descriptions = self.extract('description', response.xpath, '//td[@scope]/following-sibling::*[name() = "td" and (position() = 2)]').remove_html()
        
        output = []
        for desc in all_descriptions.data:
            strip = desc.split('</span>')[1].strip('[\n</td></p></a></b>]')

        return output
