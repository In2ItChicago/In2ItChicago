import json
import time

from event_processor.base.custom_spiders import ScraperSplashSpider
from event_processor.config import config

from scrapy_splash import SplashRequest


class FpccSpider(ScraperSplashSpider):
    """Base class for spiders that use splash for retrieving data generated through dynamic javascript content"""
    # Placeholder values that can be used if no request needs to be made through Scrapy
    allowed_domains = ['ec.samaritan.com', 'splash']
    start_urls = ['https://ec.samaritan.com/recruiter/index.php?class=RecruiterCalendar&recruiterID=1405']
    name = "fpcc"
    enabled = True

    def __init__(self, *args, **kwargs):
        super().__init__(self, 'Chicago Food Depository', 'http://splash:8050/', date_format = '%m/%d/%Y', **kwargs)


    def start_requests(self):
        """Start the request as a splash request"""
        script_to_use = self.construct_lua_click_script( \
            btn_selector='.rCalendar_tab_header', \
            content_selector='.rCalendar_tab_content:not([style*="none"])', \
            detail_selectors={ 
                'name' : '{btn}',
                'description' : '{cnt} table tr:nth-child(2)'
            }) 
        for url in self.start_urls:
            yield self.get_splash_request(url, script_to_use)

    def parse(self, response):
        jsonbody = json.loads(response.body)
        print(jsonbody)
        return None 