# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from event import Event, EventFieldData
from categories import Category
from spider_base import SpiderBase
from data_utils import DataUtils

class HistorySpider(CrawlSpider, SpiderBase):
    name = 'history'
    allowed_domains = ['www.chicagohistory.org']

    rules = (
        Rule(LinkExtractor(restrict_css = '.title'), process_request = 'link_request', callback = 'parse_item'),
    )

    def __init__(self, start_date, end_date):
        CrawlSpider.__init__(self)
        SpiderBase.__init__(self, 'https://www.chicagohistory.org/', start_date, end_date, date_format = '%d %B %Y', request_date_format = '%Y%m%d')

    def start_requests(self):
        yield self.get_request('events', {
                'start_date': self.start_date,
                'end_date': self.end_date
            })
        

    def parse_start_url(self, response):
        def get_full_date(xpath_result):
            result = []
            current_month = ''
            for text in xpath_result.data:
                text = DataUtils.remove_html(text)
                # Month names are all greater than 2 characters
                # Days of the month are all 2 characters or fewer
                if len(text) > 2:
                    current_month = text
                else:
                    result.append(f'{text} {current_month}')
            return EventFieldData(xpath_result.item, result)

        titles = self.extract('title', response.css, 'a.title::text')
        urls = self.extract('url', response.css, 'a.title::attr(href)')
        times = self.extract('time_range', response.css, '.time')
        dates = get_full_date(self.extract('date', response.css, '.xcalendar-row .number,.month'))
        descriptions = self.extract('description', response.css, '.info')

        return self.create_events('Chicago History Museum', titles, descriptions, urls, times, dates)

    def link_request(self, request):
        # Store the original url in case it gets redirected later
        request.meta['clicked_url'] = request.url
        return request

    def parse_item(self, response):
        location = self.extract('location', response.xpath, '//h3[contains(text(), "Event Location")]/following-sibling::div/p')
        price = self.extract('price', response.css, '.price').remove_whitespace()

        return Event.from_dict({
            'url': response.meta['clicked_url'],
            'address': location.data,
            'price': price.data[0] if len(price.data) > 0 else '0'
        })