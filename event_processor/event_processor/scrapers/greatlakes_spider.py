# -*- coding: utf-8 -*-
from event_processor.base.custom_spiders import ScraperSpider

class GreatLakesSpider(ScraperSpider):
    """
    This spider is unused but is being kept for now for test purposes

    greatlakes.org has an iCal feed: https://greatlakes.org/events/?ical=1&tribe_display=list
    Parsing that instead of the website would fix many of the imperfections of this scraper.
    """
    name = 'greatlakesObsolete'
    allowed_domains = ['greatlakes.org']
    enabled = False

    def __init__(self, name=None, **kwargs):
        ScraperSpider.__init__(self, 'Alliance for the Great Lakes' 'https://greatlakes.org/', date_format='%B %d',
                            request_date_format='%Y-%m-%d', **kwargs)

    def start_requests(self):
        yield self.get_request('events/', {})

    def parse(self, response):
        return {
            'title': response.css('.tribe-event-url::text').extract(),
            'url': response.css('.tribe-event-url::text').extract(),
            'event_time': self.extract_multiple(
                {'date': lambda s: s.split('@')[0], 
                'time_range': lambda s: s.split('@')[1]}, 
                response.css('.tribe-event-schedule-details').extract()),
            'address': response.css('.tribe-address').extract(),
            'description': response.css('.tribe-events-list-event-description').extract()
        }
