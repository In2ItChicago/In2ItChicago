ENABLE_API_CACHE = True
API_CACHE_EXPIRATION = 3600
API_DELAY_SECONDS = .1

ENABLE_SCRAPY_CACHE = True
SCRAPY_CACHE_EXPIRATION = 3600
VERBOSE_SCRAPY_OUTPUT = True

import os
import requests
import time
class Config:
    def __init__(self):
        self.db_client_ip = 'clipboard_db_client'
        self.db_client_port = 5000
        self.db_client_url = f'http://{self.db_client_ip}:{self.db_client_port}'

        self.db_get_events = self.db_client_url + '/events'
        self.db_put_events = self.db_client_url + '/events'
        self.db_client_status = self.db_client_url + '/status'
        
        self.debug = self.get_env_var('DEBUG', False, '0')
        self.num_connect_attempts = 10

        self.display_date_format = '%Y-%m-%d'
        self.display_time_format = '%H:%M'

    def get_env_var(self, name, error_if_null=True, default_value=None):
        try:
            return os.environ[name]
        except KeyError:
            if error_if_null:
                raise KeyError(f'Error: environment variable {name} not set. If this value was recently set, close all python processes and try again')
            else:
                return default_value
    
    def connect_to_client(self):
        for _ in range(self.num_connect_attempts):
            try:
                requests.get(self.db_client_url + '/status')
                print('Connection successful')
                return True, 'Connection successful'
            except requests.exceptions.ConnectionError:
                time.sleep(0.5)
                continue

config = Config()