from event_processor.base.custom_spiders import ApiSpider

import json


class Documenters(ApiSpider):
    """Crawler for the API on the chicago.documenters website."""
    name = 'documenters'

    start_urls = ['https://chicago.documenters.org/meetings/api/']

    def __init__(self, *args, **kwargs):
        super().__init__(self, 'Documenters',
                         'https://chicago.documenters.org/meetings/api/',
                         date_format='%Y-%m-%d', **kwargs)
        
    def parse(self, response):
        next_page_url = "first"
        while next_page_url:
            data = json.loads(response.body)
            next_page_url = data["next"]
            for e in self.get_events(data):
                yield e
            if next_page_url:
                # print(next_page_url)
                response = self.get_response(next_page_url)
                response.body = response.content

    def get_events(self, data):

        for event in data["results"]:
            category = ",".join([tag["name"] for tag in event["tags"]])
            documenters_url = "https://chicago.documenters.org/"+event["url"]
            yield {
                "title": event["name"],
                "description": event["agency"]["description"],
                "address": event["location"]["display"],
                "organization": event["agency"]["name"],
                "event_time": {
                    "date": event["start_date"],
                    "start_time": event["start_time"],
                    "end_time": event["end_time"],
                },
                "url": event["source"] or documenters_url,
                "category": category,
            }


