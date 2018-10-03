import scrapy
import os
import sys
import requests
import time
from threading import Thread
from multiprocessing import Process
from datetime import datetime
from dateutil.relativedelta import relativedelta

from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from data_aggregators.apis.library_events import LibraryEvents
from data_aggregators.apis.greatlakes_ical import GreatLakesReader
from data_aggregators.clipboard_scrapers.spiders.history_spider import HistorySpider
from data_aggregators.clipboard_scrapers.spiders.wpbcc_spider import WpbccSpider
from data_aggregators.clipboard_scrapers.spiders.lwvchicago_spider import LWVchicago

from config import config

# class ApiProcess:
#     def __init__(self):
#         self.threads = []

#     def start_api_calls(self, class_name, start_date, end_date):
#         # All api classes should take start_date and end_date as parameters to the constructor have a method called "get_events" that runs all required logic
#         api_class = class_name(start_date, end_date)
#         thread = Thread(target = api_class.get_events)
#         thread.start()
#         self.threads.append(thread)

#     def join(self):
#         for thread in self.threads:
#             thread.join()

# def connect_to_client():
#     num_attempts = 10
#     client_url = f'http://{Config.db_client_ip}:5000'
#     for i in range(num_attempts):
#         try:
#             print(f'Connecting to database client at {client_url}...')
#             requests.get(client_url + '/status')
#             print('Connection successful')
#             break
#         except requests.exceptions.ConnectionError:
#             if i == num_attempts - 1:
#                 print('Connection to db client failed. Make sure the service is running and the url is set correctly.')
#                 sys.exit(1)
#             time.sleep(0.5)

if __name__ == '__main__':
    #Config.initialize()
    status, msg = config.connect_to_client()
    if not status:
        print(msg)
        sys.exit(1)

    # get_project_settings() can't find the settings unless we execute in the same directory as scrapy.cfg
    os.chdir('data_aggregators')

    # Look for one month of events for testing purposes
    start_date = datetime.now().strftime('%m-%d-%Y')
    end_date = (datetime.now() + relativedelta(months=+1)).strftime('%m-%d-%Y')

    print('Running data engine...')

    crawlerProcess = CrawlerProcess(get_project_settings())
    #apiProcess = ApiProcess()

    crawlerProcess.crawl(HistorySpider, start_date, end_date)
    crawlerProcess.crawl(WpbccSpider, start_date, end_date)
    crawlerProcess.crawl(LWVchicago, start_date, end_date)
    crawlerProcess.crawl(LibraryEvents, start_date, end_date)
    crawlerProcess.crawl(GreatLakesReader, start_date, end_date)
    #apiProcess.start_api_calls(LibraryEvents, start_date, end_date)
    #apiProcess.start_api_calls(GreatLakesReader, start_date, end_date)

    crawlerProcess.start()
    crawlerProcess.join()
    #apiProcess.join()

    print('Data engine complete')
 
    events = requests.get(config.db_get_events, params = {
        'start_timestamp': 0, 
        'end_timestamp': 10000000000
    })

    if len(events.json()) > 0:
        print('Data retrieved successfully')
    else:
        print('No data retrieved')