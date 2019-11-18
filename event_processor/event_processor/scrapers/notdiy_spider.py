
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
        def event_date_process(str_full):
            dt_arr = str_full[0].split('~')
            if len(dt_arr) > 0:
                return [dt_arr[0]]
            return ['']
        def event_time_process(str_full):
            tm_arr = str_full[0].split('~')
            if len(tm_arr) > 0:
                return [tm_arr[2]]
            return ['']
        eresp = response.css('.inner-content')
        return {
            'title': self.empty_check_extract(eresp, self.css_func, '.page-title::text'),
            'url': self.empty_check_extract(eresp, self.css_func, 'a[href]::attr(href)'), 
            'event_time': self.create_time_data(
                date=event_date_process(self.empty_check_extract(eresp, self.css_func, '.event-date-single::text')),
                time=event_time_process(self.empty_check_extract(eresp, self.css_func, '.event-date-single::text'))
            ),
            'address': self.empty_check_extract(eresp, self.css_func, 'h3.single-event-venue::text'),
            'description': self.empty_check_extract(eresp, self.css_func, '.event-details-single::text')
        }