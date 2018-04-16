import dateutil.parser
from dateutil.relativedelta import relativedelta
from datetime import datetime
import daterangeparser
import re
import pyparsing
from data_utils import DataUtils

class TimeUtils:
    def __init__(self, old_date_format = '', new_date_format = ''):
        self.old_date_format = old_date_format
        self.new_date_format = new_date_format
        self.new_time_format = '%H:%M'

    def parse_new_or_old(self, test_string):
        try:
            return datetime.strptime(test_string, self.old_date_format)
        except ValueError:
            try:
                return datetime.strptime(test_string, self.new_date_format)
            except ValueError:
                return None

    def parse_date(self, test_string):
        test_string = DataUtils.remove_excess_spaces(test_string)
        # First, try to parse the date according the the specified formats
        parsed_date = self.parse_new_or_old(test_string)
        if parsed_date != None:
            return parsed_date, None

        try:
            # If that fails, try to parse the date as a date range string
            return daterangeparser.parse(test_string)
            
        except pyparsing.ParseException:
            # If that fails, it may be a date range in a format that daterangeparser doesn't recognize
            # Check if the string contains two formatted dates by checking the beginning and end substrings
            # until it finds two strings formatted like dates
            test_start = len(test_string) - 1
            test_end = 0
            start = None
            end = None
            while test_end < len(test_string):
                if start == None:
                    start = self.parse_new_or_old(test_string[0:test_end])
                if end == None:
                    end = self.parse_new_or_old(test_string[test_start:len(test_string)])

                if start != None and end != None:
                    break

                test_start -= 1
                test_end += 1

            if start == None or end == None:
                raise ValueError('Could not parse date string: ' + test_string)
            
            return start, end

    def get_dates(self, date_string):
        if date_string == None or len(date_string) == 0:
            return None, None
        
        start, end = self.parse_date(date_string)
        if end == None:
            return self.convert_parsed_date_format(start), None
        else:
            return self.convert_parsed_date_format(start), self.convert_parsed_date_format(end)
    
    def convert_parsed_date_format(self, parsed_date):
        now = datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)

        # We won't be querying for any dates in the past
        # If the year isn't explicitly set and the month is in the past,
        # then the event must be in the next year
        if parsed_date < now:
            parsed_date += relativedelta(years = +1)

        return parsed_date.strftime(self.new_date_format)

    def get_time(self, time_string):
        if time_string == None:
            return None
        try:
            return dateutil.parser.parse(time_string).strftime(self.new_time_format)
        # Time possibly set to something like 'All Day'
        except ValueError:
            return time_string

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
        
        # If only one time supplied, return None for the second one
        return times if len(times) > 1 else (times[0], None)

    def get_times(self, time_string):
        start_time, end_time = self.split_time(time_string)
        return self.get_time(start_time), self.get_time(end_time)

    def format_start_end(self, start, end):
        if end == None:
            end = ''
        return f'{start} - {end}'

    def parsed_day_is_between(self, parsed_test, parsed_min, parsed_max):
        if parsed_test == None:
            return False
        return parsed_min <= parsed_test <= parsed_max

    def day_is_between(self, test_date, min_date, max_date):
        parsed_min = dateutil.parser.parse(min_date)
        parsed_max = dateutil.parser.parse(max_date)
        start, end = self.parse_date(test_date)

        return self.parsed_day_is_between(start, parsed_min, parsed_max) or \
            self.parsed_day_is_between(end, parsed_min, parsed_max)