from icalendar import Calendar
from util.cache_call import cache_call
from datetime import datetime, date
from util.http_utils import HttpUtils

class ICal:
    def __init__(self, cal, default_timezone):
        self.cal = cal
        self.default_timezone = default_timezone

    @staticmethod
    def from_file(filename, default_timezone):
        with open(filename) as f:
            data = f.read()
        return ICal(Calendar.from_ical(data), default_timezone)

    @staticmethod
    @cache_call
    def from_url(url, default_timezone):
        session = HttpUtils.get_session()
        r = session.get(url)
        return ICal(Calendar.from_ical(r.text), default_timezone)

    def parse_events(self):
        org = self.cal.get('X-WR-CALNAME', 'Unknown Organization')
        return [self.create_event(event, org) for event in self.cal.subcomponents if event.name == 'VEVENT']

    # TODO Double-check that unicode is handled correctly
    def create_event(self, event, org):
        start_time = int(self.localize_min(event.get('DTSTART', '').dt).timestamp())
        end_time = int(self.localize_max(event.get('DTEND', '').dt).timestamp())
        return {
            'event_time': {
                'start_timestamp': start_time,
                'end_timestamp': end_time,
            },
            'title': '' + event.get('SUMMARY', ''),
            'description': '' + event.get('DESCRIPTION', ''),
            'address': '' + event.get('LOCATION', ''),
            'url': '' + event.get('URL', ''),
            'organization': '' + org
        }

    def localize_min(self, time):
        return self.localize(time, datetime.min.time())

    def localize_max(self, time):
        return self.localize(time, datetime.max.time())

    def localize(self, time, default_time):
        if type(time) == date:
            time = datetime.combine(time, default_time)

        if time.tzinfo is None:
            return self.default_timezone.localize(time)
        return time
