import os
import json
from time_utils import TimeUtils
from bs4 import BeautifulSoup

class AggregatorBase:
    # This class includes functionality that should be shared by spiders and API-based classes

    def __init__(self, base_url, start_date, end_date, date_format):
        # date_format is the string that specifies the date style of the target website
        time_helper = TimeUtils(date_format)
        self.base_url = base_url
        self.start_date = time_helper.get_date(start_date)
        self.end_date = time_helper.get_date(end_date)

    def remove_html(self, html_data):
        if isinstance(html_data, list):
            return [self.remove_html(data) for data in html_data]

        return BeautifulSoup(html_data, 'lxml').extract().text

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