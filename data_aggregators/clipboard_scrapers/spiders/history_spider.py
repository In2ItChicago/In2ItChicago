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
            current_month = ''
            for text in xpath_result:
                if len(text) > 2:
                    current_month = text
                else:
                    yield '{0} {1}'.format(text, current_month)

        titles = self.css_extract(response, 'a.title::text')
        links = self.css_extract(response, 'a.title::attr(href)')
        # xpath doesn't return anything when the text is empty
        times = self.css_remove_html(response, '.time')
        # xpath splits up the text when it contains html tags
        days = get_full_date(self.xpath_extract(response, '''//div[contains(@class, "xcalendar-row")]//div[@class="number" or @class="month"]/span/text() |
                                        //div[contains(@class, "xcalendar-row")]//div[@class="number" or @class="month"]/text()'''))
        descriptions = self.css_remove_html(response, '.info')

        for item in zip(titles, descriptions, links, times, days):
            yield Event(
                organization = 'Chicago History Museum',
                title = item[0],
                description = item[1],
                url = item[2],
                time_range = item[3],
                date = item[4]
            )

    def link_request(self, request):
        request.meta['clicked_url'] = request.url
        return request

    def parse_item(self, response):
        location = self.xpath_remove_html(response, '//h3[contains(text(), "Event Location")]/following-sibling::div/p')
        return Event(
            url = response.meta['clicked_url'],
            address = location
        )