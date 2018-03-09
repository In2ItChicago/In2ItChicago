# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib import parse

import sys
import os
sys.path.append(os.path.abspath('..'))
from event import Event
from categories import Category

class HistorySpider(CrawlSpider):
    name = 'history'
    allowed_domains = ['www.chicagohistory.org']

    rules = (
        Rule(LinkExtractor(restrict_css = '.title'), callback = 'parse_item'),
    )

    def __init__(self, start_date, end_date):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.base_url = 'https://www.chicagohistory.org/'

    def get_request(self, url, request_params):
        return scrapy.Request('{0}{1}?{2}'.format(self.base_url, url, parse.urlencode(request_params)))

    def start_requests(self):
        yield self.get_request('events/', {
                'start_date': '20180304',
                'end_date': '20180420'
            })
        

    def parse_start_url(self, response):
        titles = response.css('a.title::text').extract()
        links = response.css('a.title::attr(href)').extract()
        times = response.css('a.time::text').extract()
        days = response.css('a.days::text').extract()
        descriptions = response.css('.info::text').extract()

        for item in zip(titles, descriptions, links):
            yield Event(
                organization = 'Chicago History Museum',
                title = item[0],
                description = item[1],
                url = item[2]
            )

    def parse_item(self, response):
        location = response.selector.xpath('//h3[contains(text(), "Event Location")]/following-sibling::div/p/text()').extract()
        return Event(
            url = response.url,
            address = location
        )

    def closed(self, reason):
        print(reason)
