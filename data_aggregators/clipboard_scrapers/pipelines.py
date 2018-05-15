# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from event import EventManager
import requests
import json

class ClipboardPipeline(object):
    def __init__(self):
        super().__init__()
        self.event_manager = EventManager()
        
    def process_item(self, item, spider):
        self.event_manager.update(item['url'], item)
        return item

    def close_spider(self, spider):
        if len(self.event_manager.events) == 0:
            print('No data returned for ' + spider.base_url)
        spider.save_events([event.to_dict() for event in list(self.event_manager.events.values())])
