import scrapy
import os
import sys
import requests
import time
import ptvsd

from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import config 
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import spiderloader
from scrapy.utils import project

from config import config

def run():
    status, msg = config.connect_to_client()
    if not status:
       print(msg)
       sys.exit(1)

    print('Running event processor...')

    crawlerProcess = CrawlerProcess(get_project_settings())

    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    classes = [s for s in (spider_loader.load(name) for name in spiders) if s.enabled]

    crawlerProcess = CrawlerProcess(get_project_settings())

    for spider_class in classes:
        crawlerProcess.crawl(spider_class)

    crawlerProcess.start()
    crawlerProcess.join()

    print('Event processor completed')
 
    events = requests.get(config.get_events, params = {
        'start_timestamp': 0,
        'end_timestamp': 10000000000
    })

    if len(events.json()) > 0:
        print('Data retrieved successfully')
    else:
        print('No data retrieved')



if __name__ == '__main__':
    if config.debug:
        ptvsd.enable_attach(address=('0.0.0.0', 5860))
        ptvsd.wait_for_attach()
        
    run()