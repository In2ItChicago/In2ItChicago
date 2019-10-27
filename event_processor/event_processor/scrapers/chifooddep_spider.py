import json
import time

from event_processor.base.custom_spiders import ScraperSplashSpider
from event_processor.config import config

from scrapy_splash import SplashRequest


class ChiFoodDepositorySpider(ScraperSplashSpider):
    """Base class for spiders that use splash for retrieving data generated through dynamic javascript content"""
    # Placeholder values that can be used if no request needs to be made through Scrapy
    allowed_domains = ['chicagosfoodbank.org','volunteers.chicagosfoodbank.org']
    start_urls = ['https://volunteers.chicagosfoodbank.org/index.php?section=IndividualOpportunities&action=calendar']
    name = "chifooddep"
    enabled = True 

    # maybe define some template lua or javascript scripts for common scraping tasks??
    #   https://splash.readthedocs.io/en/stable/api.html#execute-javascript
    # mabybe a script template for "click on element" ??

    # .click on .fc-event 
    # scrape response that comes from clicking on .fc-event

    # https://splash.readthedocs.io/en/stable/scripting-ref.html#splash-select
    # https://splash.readthedocs.io/en/stable/scripting-ref.html#splash-select-all
    # https://splash.readthedocs.io/en/stable/scripting-element-object.html#splash-element-text

    # https://splash.readthedocs.io/en/stable/scripting-element-object.html#splash-element-mouse-click

    # Lua script for slash
    get_event_titles_lua = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))

            local event_elems = splash:select_all('.fc-event')
            local event_titles = {}
            local i = 0
            for _, elm in ipairs(event_elems) do
                event_titles[i] = elm:text()
                i = i + 1
            end

            return event_titles
        end 
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(self, 'Chicago Food Depository', 'http://localhost:8050/', date_format = '%m/%d/%Y', **kwargs)

    def start_requests(self):
        """Start the request as a splash request"""
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={ 'lua_source': self.get_event_titles_lua, 'html': 1 })

    def parse(self, response):
        print(type(response))
        print(response)
        for q in response.css("div.quote"):
            quote = QuoteItem()
            quote["author"] = q.css(".author::text").extract_first()
            quote["quote"] = q.css(".text::text").extract_first()
            yield quote