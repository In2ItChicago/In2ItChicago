# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from event_processor.base.custom_spiders import ScraperSpider
from scrapy.linkextractors import LinkExtractor

from event_processor.models.category import Category
from event_processor.util.data_utils import DataUtils

# https://volunteers.chicagosfoodbank.org/index.php?section=IndividualOpportunities&action=calendar

# Full event details from a POST Request
# example: https://volunteers.chicagosfoodbank.org/index.php?section=IndividualOpportunities&action=view_indv&fwID=11333&parentModule=43&renderMethod=dialog
# params: section=IndividualOpportunities&action=view_indv&fwID=11333&parentModule=43&renderMethod=dialog

class ChicagoFoodBankSpider(ScraperSpider):
    name = 'chiFoodDepository'
    allowed_domains = ['*chicagosfoodbank.org']
    enabled = False

    rules = (
        Rule(LinkExtractor(restrict_css = '.title'), process_request = 'link_request', callback = 'parse_item'),
    )

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'Greater Chicago Food Depository', 'https://volunteers.chicagosfoodbank.org/', date_format = '%d', **kwargs)

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
                time_range=self.empty_check_extract(response.css('.details'), self.css_func, '.time::text'),
                date=get_full_date(response.css('.xcalendar-row .number,.month').extract())
            ),
            'description': response.css('.info').extract()
        }

    def link_request(self, request, response):
        # Store the original url in case it gets redirected later
        request.meta['clicked_url'] = request.url
        return request

    def parse_item(self, response):
        prices = response.css('.price').extract()
        addresses = response.xpath('//h3[contains(text(), "Event Location")]/following-sibling::div/p').extract()
        address = ''
        if len(addresses) == 0:
            self.logger.warning(f'no address found for {response.url}')
        else:
            address = addresses[0]
        return {
            'url': [response.meta['clicked_url']],
            'address': [address],
            'price': [prices[0] if len(prices) > 0 else '0']
        }