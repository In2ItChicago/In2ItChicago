# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from custom_spiders import ScraperCrawlSpider
from event import Event
from categories import Category
from spider_base import SpiderBase

class LWVchicago(ScraperCrawlSpider):
    name = 'lwvchicago'

    allowed_domains = ['my.lwv.org']

    rules = (
        Rule(LinkExtractor(restrict_css = ('.field-name-node-link a')), callback = 'parse_start_url', follow = True),
    )

    def __init__(self, start_date, end_date):
        super().__init__(self, 'League of Women Voters', 'http://my.lwv.org/', start_date, 
        	end_date, date_format = '%W, %M %e, %Y')

    def start_requests(self):
        yield self.get_request('illinois/chicago/calendar')

    def parse(self, response):
        return {
            'title': response.css('.field-name-title h2 a::text').extract(),
            'event_time': self.extract_multiple({
                'date': lambda text: text.split(' - ')[0], 
                'time_range': lambda text: text.split(' - ')[1]
                }, response.css('.date-display-single::text')),
            'description': response.css('.text-secondary p').extract(),
            'url': response.css('.field-name-node-link a::attr(href)').extract()
        }

