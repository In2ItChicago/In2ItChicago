from custom_spiders import ApiSpider
import feedparser
from scrapy.http import HtmlResponse
class LWVChicago(ApiSpider):
    allowed_domains = ['my.lwv.org']
    start_urls = ['https://my.lwv.org/illinois/chicago/calendar']
    name = 'LWVChicago'

    def __init__(self, start_date, end_date):
        super().__init__(self, 'League of Women Voters', 'https://my.lwv.org/', start_date, end_date, date_format = '%Y-%m-%d')
    
    def parse(self, response):
        feed_url = response.css('a.feed-icon::attr(href)').extract()
        feed = feedparser.parse(feed_url)

        for entry in feed['entries']:
            detail = HtmlResponse(url='string', body=entry['summary'], encoding='utf-8')
            yield {
                'address': [detail.css('[itemprop="streetAddress"]::text').extract()],
                
            }