import scrapy

class Event(scrapy.Item):
    organization = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    date = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()

    def update(self, event):
        for key, value in event.items():
            self[key] = value

    def props_to_csv(self):
        return ','.join(self.keys()) + '\n'

    def vals_to_csv(self):
        return ','.join('"{0}"'.format(str(self[key]).replace('"', '')) for key in self.keys()) + '\n'

class EventManager(object):
    def __init__(self):
        self.events = {}
    
    def update(self, key, event):
        # Add properties to the event if it has been created already, else create a new event
        if key in self.events:
            self.events[key].update(event)
        else:
            self.events[key] = event