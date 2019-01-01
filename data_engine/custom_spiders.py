from scrapy.spiders import Spider, CrawlSpider
from spider_base import SpiderBase
from api_base import ApiBase
api_settings = {
        'ITEM_PIPELINES': {
            'clipboard_scrapers.pipelines.EventTransformPipeline': 300,
            'clipboard_scrapers.pipelines.EventBuildPipeline': 400,
            'clipboard_scrapers.pipelines.EventSavePipeline': 500
            
        }
    }
scraper_settings = {
        'ITEM_PIPELINES': {
            'clipboard_scrapers.pipelines.EventTransformPipeline': 300,
            'clipboard_scrapers.pipelines.EventBuildPipeline': 400,
            'clipboard_scrapers.pipelines.EventSavePipeline': 500
        },
        'SPIDER_MIDDLEWARES': {
            'clipboard_scrapers.middlewares.SplitItemsMiddleware': 200
        }
    }
class ApiSpider(Spider, ApiBase):
    custom_settings = api_settings
    def __init__(self, *args, **kwargs):
        Spider.__init__(self)
        ApiBase.__init__(*args, **kwargs)

class ScraperSpider(Spider, SpiderBase):
    custom_settings = scraper_settings
    def __init__(self, *args, **kwargs):
        Spider.__init__(self)
        SpiderBase.__init__(*args, **kwargs)

class ScraperCrawlSpider(CrawlSpider, SpiderBase):
    custom_settings = scraper_settings
    def __init__(self, *args, **kwargs):
        CrawlSpider.__init__(self)
        SpiderBase.__init__(*args, **kwargs)