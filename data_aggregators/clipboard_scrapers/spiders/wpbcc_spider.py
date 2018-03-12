# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib import parse

from event import Event
from categories import Category
from spider_base import SpiderBase

class WpbccSpider(CrawlSpider, SpiderBase):
    name = 'wpbcc'
    allowed_domains = ['www.wickerparkbucktown.com']

    rules = (
        Rule(LinkExtractor(restrict_css = ('.prevnextWindow', '.prevnextWindowArrow')), callback = 'parse_start_url', follow = True),
    )

    def __init__(self, start_date, end_date):
        CrawlSpider.__init__(self)
        SpiderBase.__init__(self, 'http://www.wickerparkbucktown.com/', start_date, end_date)

    def start_requests(self):
        yield self.get_request('events/', {
                'mrkrs': 'Chamber'
            })
        
    def parse_start_url(self, response):
        return self.parse_link(response)

    def parse_link(self, response):
        titles = response.css('.listerItem h2 a::text').extract()
        links = response.css('.listerItem h2 a::attr(href)').extract()
        times = response.selector.xpath('//span[contains(text(), "Time: ")]/following-sibling::text()').extract()
        days = response.selector.xpath('//span[contains(text(), "Date: ")]/following-sibling::text()').extract()
        locations = response.selector.xpath('//span[contains(text(), "Address: ")]/following-sibling::text()').extract()
        descriptions = response.css('.blurb::text').extract()

        for item in zip(titles, descriptions, links, days):
            yield Event(
                organization = 'Wicker Park and Bucktown Chamber of Commerce',
                title = item[0],
                description = item[1],
                url = item[2]
            )