import json
import time
import urllib
import random 

from event_processor.base.aggregator_base import AggregatorBase
from event_processor.config import config

from scrapy_splash import SplashRequest

class SplashBase(AggregatorBase):
    """Base class for spiders that use splash for retrieving data generated through dynamic javascript content"""
    
    active_script = ''

    def __init__(self, *args, **kwargs):
        random.seed() 
        super().__init__(*args, **kwargs)

    def get_splash_request(self, base_url, script_to_use):
        h = random.randint(1, 99)
        return SplashRequest(url=(base_url + "&h=" + str(h)), callback=self.parse, cache_args=['lua_source'], endpoint='execute', args={ 'lua_source': script_to_use, 'html' : 1 })

    def construct_lua_click_script(self, btn_selector, detail_selectors, content_selector='', retry_attempts=5):
        """Returns a lua script which will attempt to extract content from the page by first clicking 
            on a button which is selected from btn_selector, then after a delay, will try to get 
            content using the detail_selectors and the optional content_selector. It will try to 
            extract data every second for retry_attempts number of times, which is 5 by default. """
        detail_selector_part = ''
        for key in detail_selectors:
            detail_selector_part += "detail_selectors['" + key + "'] = '" + detail_selectors[key] + "'\n" 
        return '''
            json = require("json")
            treat = require("treat")

            function light_string_rep(val, val_find, val_rep)
            local vf_start, vf_end = string.find(val, val_find)
            if vf_start ~= nil then
                local first_half = ''
                if vf_start > 1 then 
                first_half = string.sub(val, 1, vf_start - 1)
                end
                local second_half = ''
                if vf_end < string.len(val) then 
                second_half = string.sub(val, vf_end + 1)
                end 
                return first_half .. val_rep .. second_half
            end 
            return val 
            end

            function main(splash, args)
                splash:go(args.url)
                splash:wait(3)
                splash.response_body_enabled = true

                local btn_selector = '__%BTN_SELECTOR%__'
                local content_selector = '__%CONTENT_SELECTOR%__'
                local detail_selectors = {}
                __%DETAIL_SELECTOR_PART%__
                local retry_attempts = __%RETRY_ATTEMPTS%__

                local btns = splash:select_all(btn_selector)
                local event_data = {}
                local i = 0
                for _, btn in ipairs(btns) do
                    event_data[i] = {}
                    btn:mouse_click{}
                    splash:wait(2)
                
                    for k, v in pairs(detail_selectors) do
                        local sel = light_string_rep(light_string_rep(v, "{btn}", btn_selector), "{cnt}", content_selector)
                        local attempts = 0
                        while attempts < retry_attempts and attempts >= 0 do
                            local elm = splash:select(sel)
                            if elm ~= nil and elm:exists() then 
                                event_data[i][k] = elm:text()
                                attempts = -1
                            else
                                attempts = attempts + 1
                                splash:wait(1)
                            end 
                        end
                        
                        event_data[i][k .. "_sel"] = sel
                        
                        if attempts == retry_attempts then
                            event_data[i][k] = '___max_attempts'
                        end 
                    end 

                    i = i + 1 
                end

                treat.as_string(event_data)
                return json.encode(event_data)
            end 
        '''.replace("__%BTN_SELECTOR%__", btn_selector) \
            .replace("__%CONTENT_SELECTOR%__", content_selector) \
            .replace("__%DETAIL_SELECTOR_PART%__", detail_selector_part) \
            .replace("__%RETRY_ATTEMPTS%__", str(retry_attempts))

