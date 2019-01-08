# -*- coding: utf-8 -*-
from custom_spiders import ScraperSpider

from data_utils import DataUtils

# This spider is unused but is being kept for now for test purposes

# greatlakes.org has an iCal feed: https://greatlakes.org/events/?ical=1&tribe_display=list
# Parsing that instead of the website would fix many of the imperfections of this scraper.
class GreatLakesSpider(ScraperSpider):
    name = 'greatlakes'
    allowed_domains = ['greatlakes.org']

    def __init__(self, start_date, end_date):
        ScraperSpider.__init__(self, 'Alliance for the Great Lakes' 'https://greatlakes.org/', start_date, end_date, date_format='%B %d',
                            request_date_format='%Y-%m-%d')

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
        # titles = self.extract('title', response.css, '.tribe-event-url::text')
        # urls = self.extract('url', response.css, '.tribe-event-url::attr(href)')
        # dates, time_ranges = self.extract_multiple(
        #     {'date': lambda s: s.split('@')[0], 
        #     'time_range': lambda s: s.split('@')[1]}, 
        #     response.css, '.tribe-event-schedule-details')
        # dates.remove_html()
        # time_ranges.remove_html()
        # addresses = self.extract('address', response.css, '.tribe-address').remove_html().map(
        #     DataUtils.remove_excess_spaces)
        # descriptions = self.extract('description', response.css, '.tribe-events-list-event-description').remove_html()

        # return self.create_events('Alliance for the Great Lakes', titles, urls, dates, time_ranges, addresses, descriptions)
