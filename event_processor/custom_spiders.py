from scrapy.spiders import Spider, CrawlSpider
from spider_base import SpiderBase
from api_base import ApiBase
api_settings = {
        'ITEM_PIPELINES': {
            'pipelines.EventTransformPipeline': 300,
            'pipelines.GeocodePipeline': 400,
            'pipelines.EventBuildPipeline': 500,
            'pipelines.EventSavePipeline': 600
        }
    }
scraper_settings = {
        'ITEM_PIPELINES': {
            'pipelines.EventTransformPipeline': 300,
            'pipelines.GeocodePipeline': 400,
            'pipelines.EventBuildPipeline': 500,
            'pipelines.EventSavePipeline': 600
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
            'middlewares.SplitItemsMiddleware': 400
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter'
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