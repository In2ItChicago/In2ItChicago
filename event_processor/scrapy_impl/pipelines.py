# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from models.event import EventManager, Event, EventLoader
from util.object_hash import ObjectHash
from threading import Lock
from config import config
from util.data_utils import DataUtils
from util.time_utils import TimeUtils
from scrapy.exceptions import DropItem
from datetime import datetime
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
                geocode = requests.get(config.get_geocode, {'address': item['address']})
                geocode_json = geocode.json()
                if geocode_json == []:
                    spider.logger.warning(f'No geocode response for address {item["address"]}')
                    return item
                item['geocode_id'] = geocode_json['id']
            except Exception as e:
                spider.logger.warning(f'Exception while getting geocode for address {item["address"]}: {e}')
        return item

class EventBuildPipeline:
    def process_item(self, item, spider):
        spider.event_manager.update(item['url'], item)
        return item

class EventSavePipeline:
    def close_spider(self, spider):
        if len(spider.event_manager.events) == 0:
            spider.logger.info(f'No data returned for ' + spider.base_url)
        else:
            self.save_events(spider)
        if config.run_scheduler:
            spider.notify_spider_complete()

    def save_events(self, spider):
        event_list = spider.event_manager.to_dicts()
        new_hash = ObjectHash.create_hash(event_list)
        spider.logger.info(f'Found {len(event_list)} events for {event_list[0]["organization"]}.')
        if new_hash == ObjectHash.get(spider.identifier):
           spider.logger.info(f'Nothing to update.')
           return
        ObjectHash.set(spider.identifier, new_hash)
        if spider.is_errored:
            spider.logger.info('Errors occurred during processing so events will not be saved')
        else:
            response = requests.post(config.put_events, json=event_list)
            if not response.ok:
                raise Exception(response.text)
            else:
                spider.logger.info(f'Saved {len(event_list)} events for {event_list[0]["organization"]}')