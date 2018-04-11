# -*- coding: utf-8 -*-
from scrapy.spiders import Spider

from spider_base import SpiderBase


# greatlakes.org has an iCal feed: https://greatlakes.org/events/?ical=1&tribe_display=list
# Parsing that instead of the website would fix many of the imperfections of this scraper.
class GreatLakesSpider(Spider, SpiderBase):
  name = 'greatlakes'
  allowed_domains = ['greatlakes.org']

  def __init__(self, start_date, end_date):
    Spider.__init__(self)
    SpiderBase.__init__(self, 'https://greatlakes.org/', start_date, end_date, date_format='%B %d, %Y')

  def start_requests(self):
    yield self.get_request('events/', {})

  def parse(self, response):
    return self.parse_link(response)

  def parse_link(self, response):
    titles = self.css_extract('title', response, '.tribe-event-url::text')
    urls = self.css_extract('url', response, '.tribe-event-url::attr(href)')
    [start_dates, start_times, end_times] = list(map(list, zip(*map(self.parse_times, response.css('.tribe-event-schedule-details')))))
    dates = self.KeyValuePair('date', start_dates)
    starts = self.KeyValuePair('start_time', start_times)
    ends = self.KeyValuePair('end_time', end_times)
    addresses = self.KeyValuePair('address', list(map(self.all_text, response.css('.tribe-address'))))
    descriptions = self.css_remove_html('description', response, '.tribe-events-list-event-description')

    for event in self.create_events(titles, urls, dates, starts, ends, addresses, descriptions):
      if self.time_utils.day_is_between(event['date'], self.start_date, self.end_date):
        event['organization'] = 'Alliance for the Great Lakes'
        yield event

  # This is not quite sufficient for parsing the address, because the comma after the city is its own entity.
  # Addresses will be formatted as "Chicago , IL 60606" (note the extra space before the comma).
  def all_text(self, selector):
    return ' '.join([x.strip() for x in selector.css('::text').extract() if x.strip()])

  # The year is implied. Events next year will appear in the past.
  # The end date is also implied. If the event ends after midnight, the end date will be wrong.
  def parse_times(self, times):
    [date, start_time] = times.css('.tribe-event-date-start::text').extract_first().split('@')
    end_time = times.css('.tribe-event-time::text').extract_first()
    return date, start_time, end_time
