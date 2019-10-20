# -*- coding: utf-8 -*-
from event_processor.base.custom_spiders import ScraperSpider

class ChiHackNightSpider(ScraperSpider): 
    name = 'chihacknight'
    allowed_domains = ['chihacknight.org']
    enabled = False 

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'Chi Hack Night', 'https://chihacknight.org/', date_format='%b %d, %Y', **kwargs)

    def start_requests(self): 
        yield self.get_request('events/', {})
    
    def parse(self, response): 
        return { 
            'title': self.empty_check_extract(response.css('table tr'), self.css_func, 'td:nth-child(3) span::text'),
            'url': self.empty_check_extract(response.css('table tr'), self.css_func, 'td:nth-child(3) a::attr(href)'),
            #'event_time': 'January 1, 2022', 
            'event_time': self.create_time_data(
                date=self.empty_check_extract(response.css('table tr'), self.css_func, 'td:nth-child(1) p::text', 'Jan 01, 2012')
            ),
            'address': list(map(lambda x: '222 Merchandise Mart Plaza, Chicago, IL 60654', self.empty_check_extract(response.css('table tr'), self.css_func, 'td::text'))),
            'description': self.empty_check_extract(response.css('table tr'), self.css_func, 'td:nth-child(4)::text')
        }
                

    