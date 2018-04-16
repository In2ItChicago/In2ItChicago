from bs4 import BeautifulSoup
import re
import json
import os

class DataUtils:
    @staticmethod
    def remove_html(html_data, remove_all = False):
        # \xa0 is returned when a &nbsp is encountered
        # Add any extraneous html data not removed by lxml here
        misc_text_to_remove = r'[\xa0]'

        if isinstance(html_data, list):
            return [DataUtils.remove_html(data, remove_all) for data in html_data]

        html_removed = BeautifulSoup(html_data, 'lxml').extract().text.strip()
        misc_removed = re.sub(misc_text_to_remove, '', html_removed, re.UNICODE)
        if not remove_all:
            return misc_removed
        # Optionally remove all non-word characters and newlines (everything except numbers and letters)
        return re.sub(r'\W+', '', misc_removed , re.UNICODE)

    @staticmethod
    def remove_excess_spaces(string):
        return re.sub(r'\s+', ' ', string.strip())

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