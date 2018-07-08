from icalendar import Calendar
from event import Event
from cache_call import cache_call
import requests

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
        r = requests.get(url)
        return ICal(Calendar.from_ical(r.text), default_timezone)

    def parse_events(self):
        org = self.cal.get('X-WR-CALNAME', 'Unknown Organization')
        return [self.create_event(event, org) for event in self.cal.subcomponents if event.name == 'VEVENT']

    # TODO Double-check that unicode is handled correctly
    def create_event(self, event, org):
        start_time = int(self.localize(event.get('DTSTART', '').dt).timestamp())
        end_time = int(self.localize(event.get('DTEND', '').dt).timestamp())
        return Event.from_dict({
            'start_timestamp': start_time,
            'end_timestamp': end_time,
            'title': '' + event.get('SUMMARY', ''),
            'description': '' + event.get('DESCRIPTION', ''),
            'address': '' + event.get('LOCATION', ''),
            'url': '' + event.get('URL', ''),
            'organization': '' + org
        })

    def localize(self, time):
        if time.tzinfo is None:
            return self.default_timezone.localize(time)
        return time
