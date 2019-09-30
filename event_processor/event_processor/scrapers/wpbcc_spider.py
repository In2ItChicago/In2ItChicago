# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from event_processor.base.custom_spiders import ScraperCrawlSpider
from scrapy.linkextractors import LinkExtractor

from event_processor.models.category import Category

class WpbccSpider(ScraperCrawlSpider):
    name = 'wpbcc'
    allowed_domains = ['www.wickerparkbucktown.com']

    rules = (
        Rule(LinkExtractor(restrict_css = ('.prevnextLink')), callback = 'parse_start_url', follow = True),
    )

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'Wicker Park/Bucktown Chamber of Commerce', 'http://www.wickerparkbucktown.com/', date_format = '%B %d, %Y', **kwargs)

    def start_requests(self):
        yield self.get_request('events/', {
                'mrkrs': 'Chamber'
            })

    def parse_start_url(self, response):
        base_selector = response.css('.listerContent')
        def sibling_extract(field):
            return self.empty_check_extract(base_selector, self.xpath_func, f'div/span[contains(text(), "{field}: ")]/following-sibling::text()')
        
        return {
            'title': response.css('.listerItem h2 a::text').extract(),
            'url': response.css('.listerItem h2 a::attr(href)').extract(),
            'event_time': self.create_time_data(time_range=sibling_extract('Time'), date=sibling_extract('Date')),
            'address': sibling_extract('Address'),
            'description': self.empty_check_extract(base_selector, self.css_func, '.blurb::text')
        }
