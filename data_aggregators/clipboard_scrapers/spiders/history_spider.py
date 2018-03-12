# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib import parse

from event import Event
from categories import Category
from spider_base import SpiderBase

class HistorySpider(CrawlSpider, SpiderBase):
    name = 'history'
    allowed_domains = ['www.chicagohistory.org']

    rules = (
        Rule(LinkExtractor(restrict_css = '.title'), callback = 'parse_item'),
    )

    def __init__(self, start_date, end_date):
        CrawlSpider.__init__(self)
        SpiderBase.__init__(self, 'https://www.chicagohistory.org/', start_date, end_date)

    def start_requests(self):
        yield self.get_request('events', {
                'start_date': self.start_date,
                'end_date': self.end_date
            })
        

    def parse_start_url(self, response):
        titles = response.css('a.title::text').extract()
        links = response.css('a.title::attr(href)').extract()
        times = response.css('a.time::text').extract()
        days = response.css('a.days::text').extract()
        descriptions = response.css('.info::text').extract()

        for item in zip(titles, descriptions, links):
            #self.event_manager.update(item[2], organization = 'Chicago History Museum', title = item[0], description = item[1], url = item[2])
            yield Event(
                organization = 'Chicago History Museum',
                title = item[0],
                description = item[1],
                url = item[2]
            )

    def parse_item(self, response):
        location = response.selector.xpath('//h3[contains(text(), "Event Location")]/following-sibling::div/p/text()').extract()
        #self.event_manager.update(response.url, address = location)
        return Event(
            url = response.url,
            address = location
        )

    def closed(self, reason):
        #print(self.event_manager.events)
        print(reason)