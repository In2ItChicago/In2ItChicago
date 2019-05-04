from scrapy.spiders import Spider, CrawlSpider
from base.spider_base import SpiderBase
from base.api_base import ApiBase
api_settings = {
        'ITEM_PIPELINES': {
            'scrapy_impl.pipelines.EventTransformPipeline': 300,
            'scrapy_impl.pipelines.GeocodePipeline': 400,
            'scrapy_impl.pipelines.EventBuildPipeline': 500,
            'scrapy_impl.pipelines.EventSavePipeline': 600
        }
    }
scraper_settings = {
        'ITEM_PIPELINES': {
            'scrapy_impl.pipelines.EventTransformPipeline': 300,
            'scrapy_impl.pipelines.GeocodePipeline': 400,
            'scrapy_impl.pipelines.EventBuildPipeline': 500,
            'scrapy_impl.pipelines.EventSavePipeline': 600
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_impl.middlewares.SplitItemsMiddleware': 400
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