from apscheduler.schedulers.twisted import TwistedScheduler
from apscheduler.events import EVENT_JOB_MISSED
from twisted.internet import reactor
from dateutil.relativedelta import relativedelta
from apis.library_events import LibraryEvents
from apis.greatlakes_ical import GreatLakesReader
from apis.lwv_chicago import LWVChicago
from scrapers.history_spider import HistorySpider
from scrapers.wpbcc_spider import WpbccSpider
from threading import Lock
from datetime import datetime
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from config import config

class Scheduler:
    def __init__(self):
        self.scrapers = [HistorySpider, WpbccSpider, LWVChicago, LibraryEvents, GreatLakesReader]
        self.interval_seconds = 60 * config.schedule_interval

        self.scheduler = TwistedScheduler()
        self.scheduler.add_listener(self.schedule_missed, EVENT_JOB_MISSED)
    
    def add_schedule(self, scraper, seconds_delay):
        self.scheduler.add_job(self.run_scraper, 
                id=scraper.__name__, 
                trigger='interval', 
                args=[scraper], 
                start_date=datetime.now() + relativedelta(seconds=seconds_delay), 
                seconds=self.interval_seconds)
        
    def schedule_missed(self, event):
        print(f'{event.job_id} missed. Interval time: {self.interval_seconds}')

    def run_scraper(self, scraper):
        start_date = datetime.now().strftime('%m-%d-%Y')
        end_date = (datetime.now() + relativedelta(months=+1)).strftime('%m-%d-%Y')
        print(f'{datetime.now()} starting {scraper.__name__}')
        runner = CrawlerRunner(get_project_settings())
        runner.crawl(scraper, start_date, end_date)
        runner.join()
    
    def run_schedule(self):
        configure_logging()
        start_interval = self.interval_seconds / len(self.scrapers)
        now = datetime.now()
        self.last_scheduled = now
        for index, scraper in enumerate(self.scrapers):
            self.add_schedule(scraper, start_interval * index)
        
        self.scheduler.start()
        reactor.run()