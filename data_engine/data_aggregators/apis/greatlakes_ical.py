from aggregator_base import AggregatorBase
from data_aggregators.apis.ical_reader import ICal
from pytz import timezone


class GreatLakesReader(AggregatorBase):
    def __init__(self, start_date, end_date):
        url = 'https://greatlakes.org/events/?ical=1&tribe_display=list'
        super().__init__(url, start_date, end_date, date_format='%Y-%m-%d')
        tz = timezone('America/Chicago')
        self.reader = ICal.from_url(self.base_url, tz)

    def get_events(self):
        events = self.reader.parse_events()
        self.save_events([event.to_dict() for event in events])
