import scrapy
import os
from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from data_aggregators.apis.library_events import LibraryEvents
from data_aggregators.clipboard_scrapers.spiders.greatlakes_spider import GreatLakesSpider
from data_aggregators.clipboard_scrapers.spiders.history_spider import HistorySpider
from data_aggregators.clipboard_scrapers.spiders.wpbcc_spider import WpbccSpider
from scraper_data import ScraperData

if __name__ == '__main__':
    # get_project_settings() can't find the settings unless we execute in the same directory as scrapy.cfg
    os.chdir('data_aggregators')

    start_date = '2018-04-09'
    end_date = '2018-05-20'

    process = CrawlerProcess(get_project_settings())
    process.crawl(HistorySpider, start_date, end_date)
    process.crawl(WpbccSpider, start_date, end_date)
    process.crawl(GreatLakesSpider, start_date, end_date)
    process.start()

    library_events = LibraryEvents(start_date, end_date)
    library_events.get_events()

    process.join()

    print(ScraperData.get_data())