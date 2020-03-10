from event_processor.base.custom_spiders import ApiSpider
from event_processor.util.data_utils import DataUtils

import json


class Documenters(ApiSpider):
    """Crawler for the API on the chicago.documenters website."""
    name = 'documenters'

    start_urls = ['https://chicago.documenters.org/search/meetings/']

    def __init__(self, *args, **kwargs):
        super().__init__(self, 'Documenters',
                        'https://chicago.documenters.org/search/meetings/',
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
    
    def get_coord(self, event, index):
        coord = DataUtils.safe_get(event, "location", "geom", "coordinates")
        if coord:
            return coord[index]
        return None

    
    
    def get_address(self, event):
        if DataUtils.safe_get(event, 'location', 'geom', 'coordinates'):
            return DataUtils.safe_get(event, "location", "display")
        elif event["location"] and event["location"]["street_address"]:
            return event["location"]["street_address"]
        elif event["location"] and event["location"]["display"]:
            return None

    def get_events(self, data):

        for event in data["results"]:
            category = ",".join([tag["name"] for tag in event["tags"]])
            documenters_url = "https://chicago.documenters.org/"+event["url"]
            if DataUtils.safe_get(event, "agency", "name") and DataUtils.safe_get(event, "location", "display"):
                yield {
                    "title": event["name"],
                    "description": DataUtils.safe_get(event, "agency", "description") or '',
                    "address": event["location"]["display"],
                    "lat": self.get_coord(event, 1),
                    "lon": self.get_coord(event, 0),
                    "organization": event["agency"]["name"],
                    "event_time": {
                        "date": event["start_date"],
                        "start_time": event["start_time"]
                    },
                    "url": DataUtils.safe_get(event, "source") or documenters_url,
                    "category": category,
                }


