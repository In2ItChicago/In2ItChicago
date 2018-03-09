# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ClipboardPipeline(object):
    def __init__(self):
        super().__init__()
        self.items = {}
        
    def process_item(self, item, spider):
        self.items[item['url']] = item
        return item
