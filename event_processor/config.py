import os
import requests
import time

class Config:
    def __init__(self):
        self.enable_api_cache = True
        self.api_cache_expiration = 3600
        self.api_delay_seconds = .1

        self.enable_scrapy_cache = True
        self.scrapy_cache_expiration = 3600
        self.verbose_scrapy_output = self.get_env_var('VERBOSE_OUTPUT', False)

        self.db_client_ip = 'event_service'
        self.db_client_port = 5000
        self.db_client_url = f'http://{self.db_client_ip}:{self.db_client_port}'

        self.db_get_events = self.db_client_url + '/events'
        self.db_put_events = self.db_client_url + '/events'
        self.db_client_status = self.db_client_url + '/status'
        
        self.debug = self.get_env_var('DEBUG', False)
        self.verbose_scrapy_output = self.get_env_var('VERBOSE_OUTPUT', False)
        self.run_scheduler = self.get_env_var('RUN_SCHEDULER', True)

        self.num_connect_attempts = 10

    def get_env_var(self, name, default_value=None, error_if_null=False):
        try:
            value = os.environ[name]
            if value == '0':
                return False
            if value == '1':
                return True
            return value
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