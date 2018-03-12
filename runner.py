import scrapy
import os
from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from data_aggregators.clipboard_scrapers.spiders.history_spider import HistorySpider
from data_aggregators.clipboard_scrapers.spiders.wpbcc_spider import WpbccSpider
from scraper_data import ScraperData

if __name__ == '__main__':
    # get_project_settings() can't find the settings unless we execute in the same directory as scrapy.cfg
    os.chdir('data_aggregators')

    process = CrawlerProcess(get_project_settings())
    process.crawl(HistorySpider, start_date='20180304', end_date='20180420')
    process.crawl(WpbccSpider, start_date='March 14, 2018', end_date='March 15, 2018')
    process.start()
    process.join()

    print(ScraperData.get_data())