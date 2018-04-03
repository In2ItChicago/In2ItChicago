import os
import json
import re
from time_utils import TimeUtils
from bs4 import BeautifulSoup

class AggregatorBase:
    # This class includes functionality that should be shared by spiders and API-based classes

    def __init__(self, base_url, start_date, end_date, date_format):
        # date_format is the string that specifies the date style of the target website
        self.time_utils = TimeUtils(date_format)
        self.base_url = base_url
        self.start_date = self.time_utils.get_date(start_date)
        self.end_date = self.time_utils.get_date(end_date)

        # \xa0 is returned when a &nbsp is encountered
        # Add any extraneous html data not removed by lxml here
        self.misc_text_to_remove = r'[\xa0]'

    def remove_html(self, html_data, remove_all = False):
        if isinstance(html_data, list):
            return [self.remove_html(data, remove_all) for data in html_data]

        html_removed = BeautifulSoup(html_data, 'lxml').extract().text
        misc_removed = re.sub(self.misc_text_to_remove, '', html_removed, re.UNICODE)
        if not remove_all:
            return misc_removed
        # Optionally remove all non-word characters and newlines (everything except numbers and letters)
        return re.sub(r'\W+', '', misc_removed , re.UNICODE)

    def pretty_json(self, json_data):
        return json.dumps(json_data, indent = 4)

    def print_json(self, json_data):
        print(self.pretty_json(json_data)) 

    def pretty_html(self, html_data):
        return BeautifulSoup(html_data, 'lxml').prettify()

    def print_html(self, html_data):
        print(self.pretty_html(html_data))

    def write_to_file(self, filename, data):
        if (os.path.isfile(filename)):
            os.remove(filename)

        with open(filename, 'w', encoding = 'utf-8') as f:
            f.writelines(data)    