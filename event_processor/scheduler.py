from apscheduler.schedulers.twisted import TwistedScheduler
from apscheduler.events import EVENT_JOB_MISSED
from twisted.internet import reactor
from dateutil.relativedelta import relativedelta
from apis.library_events import LibraryEvents
from apis.greatlakes_ical import GreatLakesReader
from apis.lwv_chicago import LWVChicago
from scrapers.spiders.history_spider import HistorySpider
from scrapers.spiders.wpbcc_spider import WpbccSpider
from threading import Lock
from datetime import datetime
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from config import config

class Scheduler:
    def __init__(self):
        self.scrapers = [HistorySpider, WpbccSpider, LWVChicago, LibraryEvents, GreatLakesReader]
        
        self.start_date = datetime.now().strftime('%m-%d-%Y')
        self.end_date = (datetime.now() + relativedelta(months=+1)).strftime('%m-%d-%Y')
        self.interval_seconds = 60 * config.schedule_interval

        self.scheduler = TwistedScheduler()
        self.scheduler.add_listener(self.schedule_missed, EVENT_JOB_MISSED)
    
    def add_schedule(self, scraper, seconds_delay):
        # Run immediately
        self.scheduler.add_job(self.run_scraper, 
                id=scraper.__name__ + 'FirstRun', 
                trigger='date', 
                args=[scraper], 
                run_date=datetime.now() + relativedelta(seconds=5 if seconds_delay == 0 else seconds_delay))
        self.scheduler.add_job(self.run_scraper, 
                id=scraper.__name__, 
                trigger='interval', 
                args=[scraper], 
                start_date=datetime.now() + relativedelta(seconds=seconds_delay), 
                seconds=self.interval_seconds)
        
    def schedule_missed(self, event):
        print(f'{event.job_id} missed. Interval time: {self.interval_seconds}')

    def run_scraper(self, scraper):
        print('starting ' + scraper.__name__)
        runner = CrawlerRunner(get_project_settings())
        runner.crawl(scraper, self.start_date, self.end_date)
        runner.join()
    
    def run_schedule(self):
        configure_logging()
        start_interval = self.interval_seconds / len(self.scrapers)
        now = datetime.now()
        self.last_scheduled = now
        self.scheduler.start()
        for index, scraper in enumerate(self.scrapers):
            self.add_schedule(scraper, start_interval * index)
        
        reactor.run()