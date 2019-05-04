from base.custom_spiders import ApiSpider
import feedparser
from scrapy.http import HtmlResponse
class LWVChicago(ApiSpider):
    allowed_domains = ['my.lwv.org']
    start_urls = ['https://my.lwv.org/illinois/chicago/calendar']
    name = 'LWVChicago'

    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'League of Women Voters', 'https://my.lwv.org/', date_format = '%Y-%m-%d', **kwargs)
    
    def parse(self, response):
        feed_url = response.css('a.feed-icon::attr(href)').extract()[0]
        feed = feedparser.parse(feed_url)

        for entry in feed['entries']:
            detail = HtmlResponse(url='string', body=entry['summary'], encoding='utf-8')
            description = detail.css('.body.text-secondary p::text').extract()
            address = detail.css('[itemprop="streetAddress"]::text').extract()
            yield {
                'address': address[0] if len(address) > 0 else '',
                'url': entry.link,
                'title': entry.title,
                'event_time': {
                    'date': detail.css('span.date-display-single::attr("content")').extract()[0].split('T')[0],
                    'time_range': detail.css('span.date-display-single::attr("content")').extract()[0].split('T')[1]
                },
                'description': description[0] if len(description) > 0 else ''
            }