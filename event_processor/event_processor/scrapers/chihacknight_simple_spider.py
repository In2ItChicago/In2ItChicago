# -*- coding: utf-8 -*-
from event_processor.base.custom_spiders import ScraperSpider

class ChiHackNightSpider(ScraperSpider): 
    name = 'chihacknight'
    allowed_domains = ['chihacknight.org']
    enabled = True 

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'Chi Hack Night', 'https://chihacknight.org/', date_format='%M %d, %Y', **kwargs)

    def start_requests(self):
        yield self.get_request('events/', {})
    