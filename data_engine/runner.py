import scrapy
import os
import sys
import requests
import argparse
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

from config import Config

class ApiProcess:
    def __init__(self):
        self.threads = []

    def start_api_calls(self, start_date, end_date, *args):
        for arg in args:
            # All api classes should take start_date and end_date as parameters to the constructor have a method called "get_events" that runs all required logic
            api_class = arg(start_date, end_date)
            thread = Thread(target = api_class.get_events)
            thread.start()
            self.threads.append(thread)

    def join(self):
        for thread in self.threads:
            thread.join()

def connect_to_client():
    num_attempts = 10
    client_url = f'http://{Config.db_client_ip}:5000'
    for i in range(num_attempts):
        try:
            print(f'Connecting to database client at {client_url}...')
            requests.get(client_url + '/status')
            print('Connection successful')
            break
        except requests.exceptions.ConnectionError:
            if i == num_attempts - 1:
                print('Connection to db client failed. Make sure the service is running and the url is set correctly.')
                sys.exit(1)
            time.sleep(0.5)

def get_env_var(name):
    try:
        return os.environ[name]
    except KeyError:
        print('Error: {0} not set. If this value was recently set, close all python processes and try again'.format(name))
        sys.exit(1)

def set_client_ip(local_dbclient):
    if local_dbclient:
        Config.db_client_ip = 'localhost'
    elif get_env_var('DB_CLIENT_IP') == '0.0.0.0':
        # data engine is running in Docker
        Config.db_client_ip = 'clipboard_db_client'
    else:
        Config.db_client_ip = get_env_var('DOCKER_IP')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--local-dbclient', action='store_true')
    args = parser.parse_args()
    
    set_client_ip(args.local_dbclient)
    connect_to_client()

    # get_project_settings() can't find the settings unless we execute in the same directory as scrapy.cfg
    os.chdir('data_aggregators')

    # Look for one month of events for testing purposes
    start_date = datetime.now().strftime('%m-%d-%Y')
    end_date = (datetime.now() + relativedelta(months=+1)).strftime('%m-%d-%Y')

    print('Running data engine...')

    crawlerProcess = CrawlerProcess(get_project_settings())
    apiProcess = ApiProcess()

    crawlerProcess.crawl(HistorySpider, start_date, end_date)
    crawlerProcess.crawl(WpbccSpider, start_date, end_date)
    crawlerProcess.crawl(LWVchicago, start_date, end_date)

    apiProcess.start_api_calls(start_date, end_date, LibraryEvents)
    apiProcess.start_api_calls(start_date, end_date, GreatLakesReader)

    crawlerProcess.start()
    crawlerProcess.join()
    apiProcess.join()

    print('Data engine complete')
 
    events = requests.get(f'http://{Config.db_client_ip}:5000/getevents', params= {
        'start_timestamp': 0, 
        'end_timestamp': 10000000000
    })

    if len(events.json()) > 0:
        print('Data retrieved successfully')