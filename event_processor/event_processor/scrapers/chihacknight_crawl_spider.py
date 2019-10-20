# -*- coding: utf-8 -*-
from event_processor.base.custom_spiders import ScraperCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class ChiHackNightCrawlSpider(ScraperCrawlSpider):
    name = 'chihacknightcrawl'
    allowed_domains = ['chihacknight.org']
    start_urls = ['https://chihacknight.org/events']
    enabled = True

    rules = (
        Rule(LinkExtractor(restrict_css = 'table tr td:nth-child(3) a'), callback="parse_page", follow=True),
    ) 
 
    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'Chi Hack Night', 'https://chihacknight.org', date_format='%B %d, %Y', **kwargs)
    
    def parse_page(self, response): 
        return {
            'title': self.empty_check_extract(response.css('#primary-content'), self.css_func, ' [itemprop="name"]::text'),
            'url': list(map(lambda x: response.url, self.empty_check_extract(response.css('#primary-content'), self.css_func, '[itemprop="name"]::text'))), 
            'event_time': self.create_time_data(
                date=self.empty_check_extract(response.css('#primary-content'), self.css_func, '[itemprop="startDate"]::text')
            ),
            'address': self.empty_check_extract(response.css('#primary-content'), self.css_func, '[itemprop="address"] *::text', default_value="222 Merchandise Mart Plaza, Chicago, IL 60654"),
            'description': self.empty_check_extract(response.css('#primary-content'), self.css_func, '[itemprop="description"] *::text')
        }