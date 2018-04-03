from dateutil.parser import parse
import re

class TimeUtils:
    def __init__(self, date_format = '', time_format = ''):
        self.date_format = date_format
        self.time_format = time_format

    def convert_datetime_format(self, datetime_string, new_format):
        try:
            return parse(datetime_string).strftime(new_format)
        except ValueError:
            return datetime_string

    def get_time(self, datetime_string):
        return self.convert_datetime_format(datetime_string, self.time_format)

    def get_date(self, datetime_string):
        return self.convert_datetime_format(datetime_string, self.date_format)

    def split_time(self, time_string):
        # Find instances of AM or PM
        am_pm = re.findall(r'[ap].?m.?', time_string, re.IGNORECASE)
        add_am_pm = ''
        if len(am_pm) == 1:
            # Only one AM/PM supplied
            # Need to make sure all times have AM or PM included

            # Get rid of all AM/PM for now, will add it to all times later
            time_string = time_string.replace(am_pm[0], '')
            add_am_pm = ' ' + am_pm[0]

        # Get times separated by '-', '–', or 'to'
        times = re.split(r'(?:-|–|to)+', time_string)

        # Add an AM/PM suffix if required, else just add an empty string    
        times = list(map((lambda time: time.strip() + add_am_pm), times))
        
        # If only one time supplied, return '' for the second one
        return times if len(times) > 1 else [times[0], '']

    def get_times(self, time_string):
        start_time, end_time = self.split_time(time_string)
        return (self.get_time(start_time), self.get_time(end_time))

    def format_start_end(self, start, end):
        return f'{start} - {end}'

    def day_is_between(self, test_date, min_date, max_date):
        return parse(min_date) <= parse(test_date) <= parse(max_date)