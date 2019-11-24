from event_processor.base.custom_spiders import ScraperNoTransposeSpider

class ForMyBlockSpider(ScraperNoTransposeSpider):
    name = 'formyblock'
    allowed_domains = ['www.formyblock.org']
    start_urls = [
        "https://www.formyblock.org/events/",
    ]
    
    def __init__(self, name=None, **kwargs):
        super().__init__(self, 'My Block, My Hood, My City', base_url='https://www.formyblock.org/', date_format = '%Y-%m-%d', **kwargs)

    def parse(self, response):
        all_future_events=response.css(".eventlist--upcoming")

        for event in all_future_events.css("article"):
            yield {
                "url": response.urljoin(event.css(".eventlist-title-link::attr(href)").get()),
                "title": event.css(".eventlist-title-link::text").get(),
                "event_time":{
                    "date": event.css(".event-date::attr(datetime)").get(),
                    "start_time": event.css(".event-time-12hr-start::text").get(),
                    "end_time": event.css(".event-time-12hr-end::text").get()
                },
                "description":event.css(".eventlist-description").get(),
                "address":event.css(".eventlist-meta-address-line::text").get(
                        default=event.css(".eventlist-meta-address::text").get(default="").strip()),
                "price":0.0,
                "organization":"My Block, My Hood, My City"  #they seem to only be publishing their own events
            }
