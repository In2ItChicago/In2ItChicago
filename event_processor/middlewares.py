# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request
import requests

class SplitItemsMiddleware:
    def get_event_count(self, item, spider):
        count = None
        for _, value in item.items():
            if count == None:
                count = len(value)
            else:
                if len(value) != count:
                    raise ValueError(f'{spider.organization}: Selectors returned data of differing lengths')
        return count

    def process_spider_output(self, response, result, spider):
        for item in result:
            if type(item) is Request:
                yield item
                continue
            event_count = self.get_event_count(item, spider)
            for processed_item in ({key: value[i] for key, value in item.items()} for i in range(event_count)):
                yield processed_item