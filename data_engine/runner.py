import scrapy
import os
import sys
import requests
import time
import ptvsd

from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import config 
from apis.library_events import LibraryEvents
from apis.greatlakes_ical import GreatLakesReader
from clipboard_scrapers.spiders.history_spider import HistorySpider
from clipboard_scrapers.spiders.wpbcc_spider import WpbccSpider
from apis.lwv_chicago import LWVChicago
from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scheduler import Scheduler

from config import config

def run():
    status, msg = config.connect_to_client()
    if not status:
       print(msg)
       sys.exit(1)

    # Look for one month of events for testing purposes
    start_date = datetime.now().strftime('%m-%d-%Y')
    end_date = (datetime.now() + relativedelta(months=+1)).strftime('%m-%d-%Y')

    print('Running data engine...')

    crawlerProcess = CrawlerProcess(get_project_settings())

    crawlerProcess.crawl(HistorySpider, start_date, end_date)
    crawlerProcess.crawl(WpbccSpider, start_date, end_date)
    crawlerProcess.crawl(LWVChicago, start_date, end_date)
    crawlerProcess.crawl(LibraryEvents, start_date, end_date)
    crawlerProcess.crawl(GreatLakesReader, start_date, end_date)

    crawlerProcess.start()
    crawlerProcess.join()

    print('Data engine complete')
 
    events = requests.get(config.db_get_events, params = {
        'start_timestamp': 0, 
        'end_timestamp': 10000000000
    })

    if len(events.json()) > 0:
        print('Data retrieved successfully')
    else:
        print('No data retrieved')



if __name__ == '__main__':
    if config.debug == "1":
        ptvsd.enable_attach(address=('0.0.0.0', 5860))
        ptvsd.wait_for_attach()
    # get_project_settings() can't find the settings unless we execute in the same directory as scrapy.cfg
    #os.chdir('data_aggregators')
    run()
    #scheduler = Scheduler()
    #scheduler.run_schedule()