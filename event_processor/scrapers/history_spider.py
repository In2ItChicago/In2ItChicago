# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from custom_spiders import ScraperCrawlSpider
from scrapy.linkextractors import LinkExtractor

from categories import Category
from spider_base import SpiderBase
from data_utils import DataUtils

class HistorySpider(ScraperCrawlSpider):
    name = 'history'
    allowed_domains = ['www.chicagohistory.org']

    rules = (
        Rule(LinkExtractor(restrict_css = '.title'), process_request = 'link_request', callback = 'parse_item'),
    )

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'Chicago History Museum', 'https://www.chicagohistory.org/', date_format = '%d %B %Y', request_date_format = '%Y%m%d', **kwargs)

    def start_requests(self):
        yield self.get_request('events', {
                'start_date': self.start_date,
                'end_date': self.end_date
            })
        

    def parse_start_url(self, response):
        def get_full_date(xpath_result):
            result = []
            current_month = ''
            for text in xpath_result:
                text = DataUtils.remove_html(text)
                # Month names are all greater than 2 characters
                # Days of the month are all 2 characters or fewer
                if len(text) > 2:
                    current_month = text
                else:
                    result.append(f'{text} {current_month}')
            return result
        
        return {
            'title': response.css('a.title::text').extract(),
            'url': response.css('a.title::attr(href)').extract(),
            'event_time': self.create_time_data(
                time_range=response.css('.time').extract(),
                date=get_full_date(response.css('.xcalendar-row .number,.month').extract())
            ),
            'description': response.css('.info').extract()
        }

    def link_request(self, request):
        # Store the original url in case it gets redirected later
        request.meta['clicked_url'] = request.url
        return request

    def parse_item(self, response):
        prices = response.css('.price').extract()
        return {
            'url': [response.meta['clicked_url']],
            'address': [response.xpath('//h3[contains(text(), "Event Location")]/following-sibling::div/p').extract()[0]],
            'price': [prices[0] if len(prices) > 0 else '0']
        }