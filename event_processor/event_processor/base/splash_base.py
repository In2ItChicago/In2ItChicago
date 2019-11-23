import json
import time
import urllib
import random 

from event_processor.base.spider_base import SpiderBase
from event_processor.config import config

from scrapy_splash import SplashRequest

class SplashBase(SpiderBase):
    """Base class for spiders that use splash for retrieving data generated through dynamic javascript content"""
    
    def __init__(self, *args, **kwargs):
        random.seed() 
        super().__init__(*args, **kwargs)

    def get_splash_requests(self, base_url, script_to_use, num_events=5, use_no_cache=True):
        use_no_cache_str = ''
        event_results = []
        # replace the {idx} tags with the index of the request on the page
        for n in range(1, num_events + 1):
            if use_no_cache:
                nocache_val = random.randint(1, 99)
                # TODO: handle cases where the URL doesn't yet have query parameters
                use_no_cache_str = "&nocache=" + str(nocache_val)
            
            event_results.append(SplashRequest(url=(base_url + use_no_cache_str), callback=self.splash_parse, 
                cache_args=['lua_source'], endpoint='execute', \
                args={ 'lua_source': script_to_use.replace('{idx}', str(n)), 'html' : 1 }))
        return event_results

    def splash_parse(self, response):
        """Internal utility function which converts the splash response to a dictionary of retrieved values.
           This function calls the splash_parse_response method which classes that inherit this kind 
           of spider should define."""
        if response == None or response.body == None:
            return None 
        json_data = None
        try:
            json_data = json.loads(response.body)
        except:
            return None
        return self.splash_parse_response(json_data) 
    
    def construct_lua_click_script(self, btn_selector, detail_selectors, content_selector='', retry_attempts=5, after_click_wait=3):
        """Returns a lua script which will attempt to extract content from the page by first clicking 
            on a button which is selected from btn_selector, then after specified delay, will try to get 
            content using the detail_selectors and the optional content_selector. It will try to 
            extract data every second for retry_attempts number of times, which is 5 by default.
            Each key in the detail_selectors dictionary will be a key in the returned event content. 
            The key 'url' is automatically populated as the url of the request."""
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
                for keyVal, btn in pairs(btns) do
                    if keyVal == {idx} then 
                        local event_data = {} 
                        event_data['url'] = args.url
                        btn:mouse_click{}
                        splash:wait(__%AFTER_CLICK_WAIT%__)
                        
                        for k, v in pairs(detail_selectors) do
                            if v == '{btn}' then
                                event_data[k] = btn:text()
                            else
                                local sel = light_string_rep(light_string_rep(v, "{btn}", btn_selector), "{cnt}", content_selector)
                                local attempts = 0
                                while attempts < retry_attempts and attempts >= 0 do
                                    local elm = splash:select(sel)
                                    if elm ~= nil and elm:exists() then 
                                        event_data[k] = elm:text()
                                        attempts = -1
                                    else
                                        attempts = attempts + 1
                                        splash:wait(1)
                                    end 
                                end
                                if attempts == retry_attempts then
                                    event_data[k] = '___max_attempts'
                                end 
                            end
                        end
                    
                        treat.as_string(event_data)
                        return json.encode(event_data)
                    end
                end
                return nil
            end 
        '''.replace("__%BTN_SELECTOR%__", btn_selector) \
            .replace("__%CONTENT_SELECTOR%__", content_selector) \
            .replace("__%DETAIL_SELECTOR_PART%__", detail_selector_part) \
            .replace("__%RETRY_ATTEMPTS%__", str(retry_attempts)) \
            .replace("__%AFTER_CLICK_WAIT%__", str(after_click_wait))
    
