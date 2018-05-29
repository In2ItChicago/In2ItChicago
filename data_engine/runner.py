import scrapy
import os
import requests
from multiprocessing import Process
from datetime import datetime
from dateutil.relativedelta import relativedelta

from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from data_aggregators.apis.library_events import LibraryEvents
from data_aggregators.clipboard_scrapers.spiders.greatlakes_spider import GreatLakesSpider
from data_aggregators.clipboard_scrapers.spiders.history_spider import HistorySpider
from data_aggregators.clipboard_scrapers.spiders.wpbcc_spider import WpbccSpider
from data_aggregators.clipboard_scrapers.spiders.lwvchicago_spider import LWVchicago

class ApiProcess:
    def __init__(self):
        self.processes = []

    def start_api_calls(self, start_date, end_date, *args):
        for arg in args:
            api_class = arg(start_date, end_date)
            p = Process(target = api_class.get_events)
            p.start()
            self.processes.append(p)

    def join(self):
        for p in self.processes:
            p.join()

if __name__ == '__main__':
    # get_project_settings() can't find the settings unless we execute in the same directory as scrapy.cfg
    os.chdir('data_aggregators')

    # Look for one month of events for testing purposes
    start_date = datetime.now().strftime('%m-%d-%Y')
    end_date = (datetime.now() + relativedelta(months=+1)).strftime('%m-%d-%Y')

    crawlerProcess = CrawlerProcess(get_project_settings())
    apiProcess = ApiProcess()

    crawlerProcess.crawl(HistorySpider, start_date, end_date)
    crawlerProcess.crawl(WpbccSpider, start_date, end_date)
    crawlerProcess.crawl(GreatLakesSpider, start_date, end_date)
    crawlerProcess.crawl(LWVchicago, start_date, end_date)

    apiProcess.start_api_calls(start_date, end_date, LibraryEvents)
    crawlerProcess.start()
    crawlerProcess.join()
    apiProcess.join()
 
    events = requests.get(f'http://{os.environ["DOCKER_IP"]}:5000/getevents', params= {
        'start_timestamp': 0, 
        'end_timestamp': 10000000000
    })
    print(events.json())