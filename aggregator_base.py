import os
import json
import re
from time_utils import TimeUtils
from bs4 import BeautifulSoup

class AggregatorBase:
    # This class includes functionality that should be shared by spiders and API-based classes

    def __init__(self, base_url, start_date, end_date, date_format, request_date_format = None):
        # date_format is the string that specifies the date style of the target website
        if request_date_format == None:
            request_date_format = date_format

        self.time_utils = TimeUtils(old_date_format=date_format, new_date_format='%m-%d-%Y')
        self.base_url = base_url
        
        request_format_utils = TimeUtils(old_date_format='%m-%d-%Y', new_date_format=request_date_format)
        self.start_date = request_format_utils.get_dates(start_date)[0]
        self.end_date = request_format_utils.get_dates(end_date)[0]