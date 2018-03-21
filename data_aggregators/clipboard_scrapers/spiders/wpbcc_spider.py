# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

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
        SpiderBase.__init__(self, 'http://www.wickerparkbucktown.com/', start_date, end_date, date_format = '%B %d, %Y')

    def start_requests(self):
        yield self.get_request('events/', {
                'mrkrs': 'Chamber'
            })
        
    def parse_start_url(self, response):
        return self.parse_link(response)

    def parse_link(self, response):
        titles = self.css_extract(response, '.listerItem h2 a::text')
        links = self.css_extract(response, '.listerItem h2 a::attr(href)')
        times = self.xpath_extract(response, '//span[contains(text(), "Time: ")]/following-sibling::text()')
        days = self.xpath_extract(response, '//span[contains(text(), "Date: ")]/following-sibling::text()')
        locations = self.xpath_extract(response, '//span[contains(text(), "Address: ")]/following-sibling::text()')
        descriptions = self.css_extract(response, '.blurb::text')

        for item in zip(titles, descriptions, links, days):
            yield Event(
                organization = 'Wicker Park and Bucktown Chamber of Commerce',
                title = item[0],
                description = item[1],
                url = item[2]
            )