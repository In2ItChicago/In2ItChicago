import scrapy
import os
import sys
import requests
import time
from threading import Thread, Lock
from multiprocessing import Process
from datetime import datetime
from dateutil.relativedelta import relativedelta

from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor

from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings

from data_aggregators.apis.library_events import LibraryEvents
from data_aggregators.apis.greatlakes_ical import GreatLakesReader
from data_aggregators.clipboard_scrapers.spiders.history_spider import HistorySpider
from data_aggregators.clipboard_scrapers.spiders.wpbcc_spider import WpbccSpider
from data_aggregators.clipboard_scrapers.spiders.lwvchicago_spider import LWVchicago


from config import config

def run():
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

    crawlerProcess.crawl(HistorySpider, start_date, end_date)
    crawlerProcess.crawl(WpbccSpider, start_date, end_date)
    crawlerProcess.crawl(LWVchicago, start_date, end_date)
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

class Scheduler:
    def __init__(self):
        self.scrapers = [HistorySpider, WpbccSpider, LWVchicago, LibraryEvents, GreatLakesReader]
        self.scheduler = TwistedScheduler()
        self.start_date = datetime.now().strftime('%m-%d-%Y')
        self.end_date = (datetime.now() + relativedelta(months=+1)).strftime('%m-%d-%Y')
        self.interval_seconds = 5
        self.delta = self.interval_seconds / len(self.scrapers)
        self.add_schedule_lock = Lock()

    def run_scraper(self, scraper):
        print('starting ' + scraper.__name__)
        runner = CrawlerRunner()
        runner.crawl(scraper, self.start_date, self.end_date)
        d = runner.join()
        next_run = datetime.now() + relativedelta(seconds=self.interval_seconds)
        d.addBoth(lambda _: self.add_run(scraper, next_run))
        print('finished ' + scraper.__name__)

    def add_run(self, scraper, date):
        with self.add_schedule_lock:
            self.scheduler.add_job(self.run_scraper, trigger='date', args=[scraper], run_date=date)
            print(f'schedule added: {scraper.__name__} at {date}')

    def run_schedule(self):
        now = datetime.now()
        for count, scraper in enumerate(self.scrapers):
            first_run = now + relativedelta(seconds=count*self.delta)
            self.add_run(scraper, first_run)
        
        self.scheduler.start()
        reactor.run()

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run_schedule()