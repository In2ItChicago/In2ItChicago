import json
import time
import re 
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
        super().__init__(self, 'Forest Preserves of Cook County', 'http://splash:8050/', date_format = '%d %b %Y', **kwargs)

    def start_requests(self):
        """Start the request as a splash request"""
        script_to_use = self.construct_lua_click_script( \
            btn_selector='.rCalendar_tab_header', \
            content_selector='.rCalendar_tab_content:not([style*="none"])', \
            detail_selectors={ 
                'title' : '{btn}',
                'description' : '{cnt} table tr:nth-child(2)',
                'date_unparsed' : '{cnt} table tr:nth-child(6) p:nth-child(1)',
                'address' : '{cnt} table tr:nth-child(8) div'
            },
            after_click_wait=3 # wait 3 seconds after clicking on the button before trying to extract content
            ) 
        for url in self.start_urls:
            for res in self.get_splash_requests(url, script_to_use, 8):
                yield res 

    def splash_parse_response(self, response): 
        # extract the two times
        # get all the strings before the two times 
        if 'title' in response:
            find_start_time = ''
            find_end_time = ''
            extract_times = re.findall("([0-9]?[0-9]:[0-9][0-9] [ap]m)", response['date_unparsed'])
            if len(extract_times) > 0:
                find_start_time = extract_times[0]
            if len(extract_times) > 1:
                find_end_time = extract_times[1]

            extract_date = response['date_unparsed']
            time_find_index = response['date_unparsed'].index(extract_times[0])
            if time_find_index != None and time_find_index >= 0:
                extract_date = response['date_unparsed'][:(time_find_index - 1)]
                
            return {
                'title' : [ response['title'] ],
                'url' : [ response['url'] ],
                'description' : [ response['description'] ],
                'event_time' : self.create_time_data(
                    date=[ extract_date ], 
                    start_time=[ find_start_time ],
                    end_time=[ find_end_time ]
                ),
                'address' : [ response['address'].replace("View map", "") ], 
                'category' : [ 'Environment' ]
            }
        return None # when title is not in response, then there was an error extracting data