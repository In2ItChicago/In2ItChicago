# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from event import EventManager
from event_hashes import EventHashes
from threading import Lock
from config import config
import requests
import json

class EventBuildPipeline:
    def process_item(self, item, spider):
        spider.event_manager.update(item['url'], item)
        return item

class EventSavePipeline:
    def __init__(self):
        super().__init__()
        self.update_mutex = Lock()
        
    def close_spider(self, spider):
        if len(spider.event_manager.events) == 0:
            print('No data returned for ' + spider.base_url)
        self.save_events(spider.identifier, [event.to_dict() for event in list(spider.event_manager.events.values())])

    def save_events(self, identifier, event_list):
        if len(event_list) == 0:
            return
        new_hash = EventHashes.create_hash(event_list)
        print(f'Found {len(event_list)} events for {event_list[0]["organization"]}.')
        if new_hash == EventHashes.get(identifier):
            print('Nothing to update.')
            return
        EventHashes.set(identifier, new_hash)

        with self.update_mutex:
            response = requests.post(config.db_put_events, json=event_list)
        if not response.ok:
            raise ValueError(response.text)
        else:
            print(f'Saved {len(event_list)} events for {event_list[0]["organization"]}')