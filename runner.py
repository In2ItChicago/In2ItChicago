import scrapy
import os
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
from scraper_data import ScraperData

class ApiProcess:
    def __init__(self):
        self.processes = []

    def start_api_calls(self, *args):
        for arg in args:
            p = Process(target = arg)
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
    end_date = (datetime.now() + relativedelta(month=+1)).strftime('%m-%d-%Y')

    crawlerProcess = CrawlerProcess(get_project_settings())
    apiProcess = ApiProcess()

    crawlerProcess.crawl(HistorySpider, start_date, end_date)
    crawlerProcess.crawl(WpbccSpider, start_date, end_date)
    crawlerProcess.crawl(GreatLakesSpider, start_date, end_date)
    crawlerProcess.crawl(LWVchicago, start_date, end_date)

    library_events = LibraryEvents(start_date, end_date)
    apiProcess.start_api_calls(library_events.get_events)
    
    crawlerProcess.start()
    crawlerProcess.join()
    apiProcess.join()

    print(ScraperData.get_data())