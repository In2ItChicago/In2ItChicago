from event_processor.base.custom_spiders import ScraperSpider
import usaddress
import re
from event_processor.util.data_utils import DataUtils


class HmprgSpider(ScraperSpider):
    name = 'hmprg'
    allowed_domains = ['hmprg.org']
    enabled = True

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'Health & Medicine Policy Research Group', 'http://hmprg.org/', date_format='%b %d, %Y', **kwargs)

    def start_requests(self):
        yield self.get_request('events/', {})

    def parse(self, response):
        return {
            'title': self.empty_check_extract(response.css('article .entry.blog'), self.css_func, 'a::text'),
            'url': self.empty_check_extract(response.css('article .entry.blog'), self.css_func, 'a::attr(href)'),
            'event_time': self.create_time_data(
                date=self.empty_check_extract(response.css('article .entry.blog'), self.css_func, '.date::text', 'Jan 01, 2012')
            ),
            'address': list(map(self.__get_address, response.css('article .entry.blog'))),
            'description': self.empty_check_extract(response.css('article .entry.blog'), self.css_func, 'p')
        }

    def __get_address(self, event):
        event_body = DataUtils.remove_html(event.get())
        address_list = usaddress.parse(event_body)
        address_dict = dict(map(reversed, dict(address_list).items()))

        if "StreetName" in address_dict:
            return "{0} {1} {2} {3}, {4} {5} {6}".format(address_dict['AddressNumber'],
                                                        address_dict['StreetNamePreDirectional'],
                                                        address_dict['StreetName'],
                                                        address_dict['StreetNamePostType'],
                                                        address_dict['PlaceName'],
                                                        address_dict['StateName'],
                                                        address_dict['ZipCode'])
        elif re.search(r"Webinar", event_body):
            return "Webinar: {0}".format(self.empty_check_extract([event], self.css_func, 'a::attr(href)')[0])
        else:
            return ""
