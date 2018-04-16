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
        base_selector = response.css('.listerContent')
        
        titles = self.extract('title', response.css, '.listerItem h2 a::text')
        urls = self.extract('url', response.css, '.listerItem h2 a::attr(href)')
        times = self.empty_check_extract('time_range', base_selector, 'xpath', 'div/span[contains(text(), "Time: ")]/following-sibling::text()')
        dates = self.empty_check_extract('date', base_selector, 'xpath', 'div/span[contains(text(), "Date: ")]/following-sibling::text()')
        addresses = self.empty_check_extract('address', base_selector, 'xpath', 'div/span[contains(text(), "Address: ")]/following-sibling::text()')
        descriptions = self.extract('description', response.css, '.blurb::text')

        for event in self.create_events(titles, urls, times, dates, addresses, descriptions):
            if self.time_utils.day_is_between(event['date'], self.start_date, self.end_date):
                event['organization'] = 'Wicker Park and Bucktown Chamber of Commerce'
                yield event
