from scrapy.spiders import Spider, CrawlSpider
from event_processor.base.spider_base import SpiderBase
from event_processor.base.api_base import ApiBase
from event_processor.base.splash_base import SplashBase
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
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
            'event_processor.scrapy_impl.middlewares.SplitItemsMiddleware': 400
        },
        'DUPEFILTER_CLASS' : 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE' : 'scrapy_splash.SplashAwareFSCacheStorage',
        'DOWNLOADER_MIDDLEWARES' : { 
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        }
    }

no_transpose_scraper_settings  = {
        'ITEM_PIPELINES': {
            'event_processor.scrapy_impl.pipelines.EventTransformPipeline': 300,
            'event_processor.scrapy_impl.pipelines.GeocodePipeline': 400,
            'event_processor.scrapy_impl.pipelines.EventBuildPipeline': 500,
            'event_processor.scrapy_impl.pipelines.EventSavePipeline': 600
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

class ScraperSplashSpider(Spider, SplashBase):
    """??? Base spider for web crawling with Splash, which can render and extract data from pages that have javascript generated dynamic content"""
    custom_settings = scraper_settings
    def __init__(self, *args, **kwargs):
        Spider.__init__(self)
        SplashBase.__init__(*args, **kwargs)

class ScraperNoTransposeSpider(Spider, SpiderBase):
    custom_settings = no_transpose_scraper_settings
    def __init__(self, *args, **kwargs):
        Spider.__init__(self)
        SpiderBase.__init__(*args, **kwargs)
