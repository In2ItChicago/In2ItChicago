import dateutil.parser
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time
import daterangeparser
import re
import pyparsing
from data_utils import DataUtils

class TimeUtils:
    def __init__(self, date_format=''):
        # date_format is the format string that represents the formatting of the date strings 
        # that will be passed in to methods in this class
        self.date_format = date_format

    def get_timestamp(self, date, time=None):
        if time != None:
            date += relativedelta(hour=time.hour, minute=time.minute)
        return self.datetime_to_timestamp(date)
    
    def get_timestamps(self, time_data):
        parsed_start_date = None
        parsed_end_date = None
        parsed_start_time = None
        parsed_end_time = None

        min_timestamp = None
        max_timestamp = None

        if time_data['start_timestamp'] != None:
            return time_data['start_timestamp'], time_data['end_timestamp']

        if time_data['date'] != None:
            parsed_start_date, parsed_end_date = self.parse_date(time_data['date'])
        elif time_data['start_date'] != None and time_data['end_date'] != None:
            parsed_start_date = self.parse_date_string(time_data['start_date'])
            parsed_end_date = self.parse_date_string(time_data['end_date'])
        else:
            raise ValueError('Either date or start and end date must be set')

        if time_data['start_time'] != None:
            parsed_start_time = self.parse_time(time_data['start_time'])
            parsed_end_time = self.parse_time(time_data['end_time'])
        elif time_data['time_range'] != None:
            parsed_start_time, parsed_end_time = self.parse_times(time_data['time_range'])
        
        if parsed_start_time == None:
            min_timestamp = self.min_timestamp_for_day(parsed_start_date)
        else:
            min_timestamp = self.get_timestamp(parsed_start_date, parsed_start_time)

        if parsed_end_time == None:
            max_timestamp = self.max_timestamp_for_day(parsed_end_date)
        else:
            max_timestamp = self.get_timestamp(parsed_end_date, parsed_end_time)

        return min_timestamp, max_timestamp

    def min_timestamp_for_day(self, date):
        if isinstance(date, str):
            date = self.parse_date_string(date)
        return self.get_timestamp(date + relativedelta(hour=0, minute=0))
    
    def max_timestamp_for_day(self, date):
        if isinstance(date, str):
            date = self.parse_date_string(date)
        return self.get_timestamp(date + relativedelta(hour=23, minute=59))
    
    def datetime_to_timestamp(self, date):
        return int(time.mktime(date.timetuple()))

    def convert_date_format(self, date_string, new_format):
        parsed_date = self.parse_date_string(date_string)
        if parsed_date == None:
            return None
        return parsed_date.strftime(new_format)

    def parse_date_string(self, test_string):
        try:
            parsed_date = datetime.strptime(test_string, self.date_format)
            parsed_date = self.set_year(parsed_date)
            now = datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)

            # We won't be querying for any dates in the past
            # If the year isn't explicitly set and the month is in the past,
            # then the event must be in the next year
            if parsed_date < now:
                parsed_date += relativedelta(years = +1)
            return parsed_date
        except ValueError:
            return None

    def parse_date(self, test_string):
        test_string = DataUtils.remove_excess_spaces(test_string)
        # First, try to parse the date according the the specified format
        parsed_date = self.parse_date_string(test_string)
        if parsed_date != None:
            return parsed_date, parsed_date
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
                    start = self.parse_date_string(test_string[0:test_end])
                if end == None:
                    end = self.parse_date_string(test_string[test_start:len(test_string)])

                if start != None and end != None:
                    break

                test_start -= 1
                test_end += 1

            if start == None or end == None:
                raise ValueError('Could not parse date string: ' + test_string)
            
            return start, end

    def set_year(self, date_obj):
        if date_obj.year == 1900:
            date_obj += relativedelta(year=datetime.now().year)
        return date_obj

    def parse_time(self, time_string):
        if time_string == None:
            return None
        try:
            return dateutil.parser.parse(time_string) #.strftime(self.new_time_format)
        # Time possibly set to something like 'All Day'
        except ValueError:
            return None

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

    def parse_times(self, time_string):
        start_time, end_time = self.split_time(time_string)
        return self.parse_time(start_time), self.parse_time(end_time)

    def format_start_end(self, start, end):
        if end == None:
            end = ''
        return f'{start} - {end}'

    def time_is_between(self, timestamp, min_timestamp, max_timestamp):
        return min_timestamp <= timestamp <= max_timestamp

    def time_range_is_between(self, start_timestamp, end_timestamp, min_timestamp, max_timestamp):
        return self.time_is_between(start_timestamp, min_timestamp, max_timestamp) and \
            self.time_is_between(end_timestamp, min_timestamp, max_timestamp)