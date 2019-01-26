from apis.ical_reader import ICal
from pytz import timezone
from custom_spiders import ApiSpider
from api_base import ApiBase

class GreatLakesReader(ApiSpider):
    name = 'greatlakes'

    def parse(self, response):
        return self.get_events()

    def __init__(self, name=None, **kwargs):
        url = 'https://greatlakes.org/events/?ical=1&tribe_display=list'
        super().__init__(self, 'Alliance for the Great Lakes', url, date_format='%Y-%m-%d')
        tz = timezone('America/Chicago')
        self.reader = ICal.from_url(self.base_url, tz)

    def get_events(self):
        return self.reader.parse_events()
