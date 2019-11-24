from scrapy.spiders import Spider, CrawlSpider
from event_processor.base.spider_base import SpiderBase
from event_processor.base.api_base import ApiBase
api_settings = {
        'ITEM_PIPELINES': {
            'event_processor.scrapy_impl.pipelines.EventTransformPipeline': 300,
            'event_processor.scrapy_impl.pipelines.GeocodePipeline': 400,
            'event_processor.scrapy_impl.pipelines.EventBuildPipeline': 500,
            'event_processor.scrapy_impl.pipelines.EventSavePipeline': 600
        }
    }
scraper_settings = {
        'ITEM_PIPELINES': {
            'event_processor.scrapy_impl.pipelines.EventTransformPipeline': 300,
            'event_processor.scrapy_impl.pipelines.GeocodePipeline': 400,
            'event_processor.scrapy_impl.pipelines.EventBuildPipeline': 500,
            'event_processor.scrapy_impl.pipelines.EventSavePipeline': 600
        },
        'SPIDER_MIDDLEWARES': {
            'event_processor.scrapy_impl.middlewares.SplitItemsMiddleware': 400
        }
    }

no_transpose_scraper_settings  = {
        'ITEM_PIPELINES': {
            'scrapy_impl.pipelines.EventTransformPipeline': 300,
            'scrapy_impl.pipelines.GeocodePipeline': 400,
            'scrapy_impl.pipelines.EventBuildPipeline': 500,
            'scrapy_impl.pipelines.EventSavePipeline': 600
        }
    }

class ApiSpider(Spider, ApiBase):
    """Base spider for reading Apis"""
    custom_settings = api_settings
    def __init__(self, *args, **kwargs):
        Spider.__init__(self)
        ApiBase.__init__(*args, **kwargs)

class ScraperSpider(Spider, SpiderBase):
    """??? Base spider for reading websites that only need a single page load"""
    custom_settings = scraper_settings
    def __init__(self, *args, **kwargs):
        Spider.__init__(self)
        SpiderBase.__init__(*args, **kwargs)

class ScraperCrawlSpider(CrawlSpider, SpiderBase):
    """??? Base spider for reading websites that may require further crawling and multiple page loads"""
    custom_settings = scraper_settings
    def __init__(self, *args, **kwargs):
        CrawlSpider.__init__(self)
        SpiderBase.__init__(*args, **kwargs)

class ScraperNoTransposeSpider(Spider, SpiderBase):
    custom_settings = no_transpose_scraper_settings
    def __init__(self, *args, **kwargs):
        Spider.__init__(self)
        SpiderBase.__init__(*args, **kwargs)

# todo; make a spider that can traverse java script click events?  