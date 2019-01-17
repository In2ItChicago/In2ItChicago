# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from event import EventManager, Event, EventLoader
from event_hashes import EventHashes
from threading import Lock
from config import config
from data_utils import DataUtils
from time_utils import TimeUtils
from scrapy.exceptions import DropItem
import requests
import json

class EventTransformPipeline:
    def __init__(self):
        self.time_utils = TimeUtils()

    def process_item(self, item, spider):
        item['organization'] = spider.organization
        if 'event_time' in item:
            item['event_time']['date_format'] = spider.date_format
        loader = EventLoader(**item)
        if 'event_time' in loader.item:
            time = loader.item['event_time']
            if self.time_utils.time_range_is_between(time['start_timestamp'], time['end_timestamp'], spider.start_timestamp, spider.end_timestamp):
                return loader.item
            else:
                raise DropItem('Event is not in the confured timeframe')
        else:
            return loader.item
            
class GeocodePipeline:
    def process_item(self, item, spider):
        if 'address' in item:
            try:
                geocode = requests.get(config.db_get_geocode, {'address': item['address']})
                item['geocode'] = geocode.json()
            except Exception as e:
                print('Exception while getting geocode: ' + str(e))
        return item

class EventBuildPipeline:
    def process_item(self, item, spider):
        spider.event_manager.update(item['url'], item)
        return item

class ScraperTransformPipeline:
    def process_item(self, item, spider):
        event_count = self.get_event_count(item, spider)
        for processed_item in ({key: value[i]} for key, value in item.items() for i in range(event_count)):
            yield processed_item
        
    
    def get_event_count(self, item, spider):
        count = None
        for _, value in item.items():
            if count == None:
                count = len(value)
            else:
                if len(value) != count:
                    raise ValueError(f'{spider.organization}: Selectors returned data of differing lengths')
        return count

class EventSavePipeline:
    def close_spider(self, spider):
        if len(spider.event_manager.events) == 0:
            print('No data returned for ' + spider.base_url)
        else:
            self.save_events(spider.identifier, spider.event_manager.to_dicts())

    def save_events(self, identifier, event_list):
        new_hash = EventHashes.create_hash(event_list)
        print(f'Found {len(event_list)} events for {event_list[0]["organization"]}.')
        if new_hash == EventHashes.get(identifier):
           print('Nothing to update.')
           return
        EventHashes.set(identifier, new_hash)

        response = requests.post(config.db_put_events, json=event_list)
        if not response.ok:
            raise ValueError(response.text)
        else:
            print(f'Saved {len(event_list)} events for {event_list[0]["organization"]}')