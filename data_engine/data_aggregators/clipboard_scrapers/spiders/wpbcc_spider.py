# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from custom_spiders import ScraperCrawlSpider
from scrapy.linkextractors import LinkExtractor

from event import Event
from categories import Category
from spider_base import SpiderBase

class WpbccSpider(ScraperCrawlSpider):
    name = 'wpbcc'
    allowed_domains = ['www.wickerparkbucktown.com']

    rules = (
        Rule(LinkExtractor(restrict_css = ('.prevnextLink')), callback = 'parse_start_url', follow = True),
    )

    def __init__(self, start_date, end_date):
        super().__init__(self, 'Wicker Park/Bucktown Chamber of Commerce', 'http://www.wickerparkbucktown.com/', start_date, end_date, date_format = '%B %d, %Y')

    def start_requests(self):
        yield self.get_request('events/', {
                'mrkrs': 'Chamber'
            })

    def parse_start_url(self, response):
        base_selector = response.css('.listerContent')
        def sibling_extract(field):
            return self.empty_check_extract(base_selector, self.xpath_func, 'div/span[contains(text(), "{0}: ")]/following-sibling::text()'.format(field))
        
        return {
            'title': response.css('.listerItem h2 a::text').extract(),
            'url': response.css('.listerItem h2 a::attr(href)').extract(),
            'event_time': self.create_time_data(time_range=sibling_extract('Time'), date=sibling_extract('Date')),
            'address': sibling_extract('Address'),
            'description': self.empty_check_extract(base_selector, self.css_func, '.blurb::text')
        }
