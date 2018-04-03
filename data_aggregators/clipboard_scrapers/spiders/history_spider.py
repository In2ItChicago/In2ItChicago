# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from event import Event
from categories import Category
from spider_base import SpiderBase

class HistorySpider(CrawlSpider, SpiderBase):
    name = 'history'
    allowed_domains = ['www.chicagohistory.org']

    rules = (
        Rule(LinkExtractor(restrict_css = '.title'), process_request = 'link_request', callback = 'parse_item'),
    )

    def __init__(self, start_date, end_date):
        CrawlSpider.__init__(self)
        SpiderBase.__init__(self, 'https://www.chicagohistory.org/', start_date, end_date, date_format = '%Y%m%d')

    def start_requests(self):
        yield self.get_request('events', {
                'start_date': self.start_date,
                'end_date': self.end_date
            })
        

    def parse_start_url(self, response):
        def get_full_date(xpath_result):
            result = []
            current_month = ''
            for text in xpath_result.value:
                # Month names are all greater than 2 characters
                # Days of the month are all 2 characters or less
                if len(text) > 2:
                    current_month = text
                else:
                    result.append(f'{text} {current_month}')
            return self.KeyValuePair(xpath_result.key, result)

        titles = self.css_extract('title', response, 'a.title::text')
        urls = self.css_extract('url', response, 'a.title::attr(href)')
        # xpath doesn't return anything when the text is empty
        times = self.css_remove_html('time_range', response, '.time')
        # xpath splits up the text when it contains html tags
        dates = get_full_date(self.xpath_extract('date', response, '''//div[contains(@class, "xcalendar-row")]//div[@class="number" or @class="month"]/span/text() |
                                        //div[contains(@class, "xcalendar-row")]//div[@class="number" or @class="month"]/text()'''))
        descriptions = self.css_remove_html('description', response, '.info')

        for event in self.create_events(titles, descriptions, urls, times, dates):
            event['organization'] = 'Chicago History Museum'
            yield event

    def link_request(self, request):
        # Store the original url in case it gets redirected later
        request.meta['clicked_url'] = request.url
        return request

    def parse_item(self, response):
        location = self.xpath_remove_html('location', response, '//h3[contains(text(), "Event Location")]/following-sibling::div/p')
        price = self.css_remove_html('price', response, '.price', remove_all=True)

        return Event(
            url = response.meta['clicked_url'],
            address = location.value,
            price = price.value[0] if len(price.value) > 0 else '0'
        )