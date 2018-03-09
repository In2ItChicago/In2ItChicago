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

    # def __init__(self, organization, title, description, address, date, start_time, end_time, url, price, category):
    #     self.organization = organization
    #     self.title = title
    #     self.description = description
    #     self.address = address
    #     self.date = date
    #     self.start_time = start_time
    #     self.end_time = end_time
    #     self.url = url
    #     self.price = price
    #     self.category = category

    def props_to_csv(self):
        return ','.join(self.keys()) + '\n'

    def vals_to_csv(self):
        return ','.join(['"{0}"'.format(str(self[key]).replace('"', '')) for key in self.keys()]) + '\n'