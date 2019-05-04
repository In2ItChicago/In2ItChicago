from bs4 import BeautifulSoup
import re
import json
import os
import warnings
# Don't show warnings about parsing urls
# This is just a side effect of passing all data to BeautifulSoup
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

class DataUtils:
    @staticmethod
    def remove_html(html_data):
        # \xa0 is returned when a &nbsp is encountered
        # Add any extraneous html data not removed by lxml here
        misc_text_to_remove = r'[\xa0]'
        
        if isinstance(html_data, list):
            return [DataUtils.remove_html(data) for data in html_data]

        if not isinstance(html_data, str):
            return html_data

        lxml_removed = BeautifulSoup(html_data, 'lxml').extract().text.strip()
        html_removed = re.sub(misc_text_to_remove, '', lxml_removed, re.UNICODE)
        spaces_removed = DataUtils.remove_excess_spaces(html_removed)

        return spaces_removed

    @staticmethod
    def remove_whitespace(html_data):
        if isinstance(html_data, list):
            return [DataUtils.remove_html(data) for data in html_data]

        return re.sub(r'\W+', '', html_data , re.UNICODE)

    @staticmethod
    def remove_excess_spaces(string):
        return re.sub(r'[ \t]+', ' ', string.strip())

    @staticmethod
    def pretty_json(json_data):
        return json.dumps(json_data, indent = 4)

    @staticmethod
    def print_json(json_data):
        print(DataUtils.pretty_json(json_data)) 

    @staticmethod
    def pretty_html(html_data):
        return BeautifulSoup(html_data, 'lxml').prettify()

    @staticmethod
    def print_html(html_data):
        print(DataUtils.pretty_html(html_data))

    @staticmethod
    def write_to_file(filename, data):
        if (os.path.isfile(filename)):
            os.remove(filename)

        with open(filename, 'w', encoding = 'utf-8') as f:
            f.writelines(data)    