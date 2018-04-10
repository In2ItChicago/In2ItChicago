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
        base_selector = response.css('.listerContent')
        
        titles = self.css_extract('title', response, '.listerItem h2 a::text')
        urls = self.css_extract('url', response, '.listerItem h2 a::attr(href)')
        times = self.xpath_empty_check_extract('time_range', base_selector, 'div/span[contains(text(), "Time: ")]/following-sibling::text()')
        #times = self.xpath_extract('time_range', response, '//span[contains(text(), "Time: ")]/following-sibling::text()')
        dates = self.xpath_empty_check_extract('date', base_selector, 'div/span[contains(text(), "Date: ")]/following-sibling::text()')
        #dates = self.xpath_extract('date', response, '//span[contains(text(), "Date: ")]/following-sibling::text()')
        addresses = self.xpath_empty_check_extract('address', base_selector, 'div/span[contains(text(), "Address: ")]/following-sibling::text()')
        #addresses = self.xpath_extract('address', response, '//span[contains(text(), "Address: ")]/following-sibling::text()')
        descriptions = self.css_extract('description', response, '.blurb::text')

        for event in self.create_events(titles, urls, times, dates, addresses, descriptions):
            if self.time_utils.day_is_between(event['date'], self.start_date, self.end_date):
                event['organization'] = 'Wicker Park and Bucktown Chamber of Commerce'
                yield event
