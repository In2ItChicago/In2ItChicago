
# this spider should try to ONLY get volunteer relevant events from DIY
# the lazy way of doing that is to try and only extract evnets with the string "volunteer" somewhere in it? 

# -*- coding: utf-8 -*-
from event_processor.base.custom_spiders import ScraperCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class NotDIYSpider(ScraperCrawlSpider):
    """This spider scrapes the not diy chi website, but will only keep events which have the keyword
        'volunteer' somewhere in its title or description."""
    name = 'notdiychi'
    allowed_domains = ['notdiychi.com']
    start_urls = ['https://notdiychi.com/']
    enabled = True

    rules = (
        Rule(LinkExtractor(restrict_css = '.inner-content .event-title a'), callback="parse_page", follow=True),
    ) 
 
    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'not diy chi', 'https://notdiychi.com/', date_format='%A, %B %d', **kwargs)
    
    def item_filter(self, item): 
        return 'volunteer' in item['title'] or 'volunteer' in item['description']

    def parse_page(self, response): 
        def event_date_extract(str_full, index_to_extract):
            dt_arr = str_full[0].split('~')
            if len(dt_arr) >= index_to_extract:
                return [dt_arr[index_to_extract]]
            return [''] 
        eresp = response.css('.inner-content')
        return {
            'title': self.empty_check_extract(eresp, self.css_func, '.page-title::text'),
            'url': self.empty_check_extract(eresp, self.css_func, 'a[href]::attr(href)'), 
            'event_time': self.create_time_data(
                date=event_date_extract(self.empty_check_extract(eresp, self.css_func, '.event-date-single::text'), 0),
                time=event_date_extract(self.empty_check_extract(eresp, self.css_func, '.event-date-single::text'), 2)
            ),
            'address': self.empty_check_extract(eresp, self.css_func, 'h3.single-event-venue::text'),
            'description': self.empty_check_extract(eresp, self.css_func, '.event-details-single::text')
        }