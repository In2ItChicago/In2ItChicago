import os
import requests
import time

class Config:
    def __init__(self):
        self.enable_api_cache = True
        self.api_cache_expiration = 3600
        self.api_delay_seconds = 0.1

        self.enable_scrapy_cache = True
        self.scrapy_cache_expiration = 3600
        self.verbose_scrapy_output = self.get_env_var('VERBOSE_OUTPUT', False)

        self.db_client_ip = 'event_service'
        self.db_client_port = 5000
        self.db_client_url = f'http://{self.db_client_ip}:{self.db_client_port}'

        self.db_get_events = self.db_client_url + '/events'
        self.db_put_events = self.db_client_url + '/events'
        self.db_get_geocode = self.db_client_url + '/geocode'
        self.db_client_status = self.db_client_url + '/status'
        
        self.debug = self.get_env_bool('DEBUG', False)
        self.verbose_scrapy_output = self.get_env_bool('VERBOSE_OUTPUT', False)
        self.run_scheduler = self.get_env_bool('RUN_SCHEDULER', True)
        self.schedule_interval = int(self.get_env_var('SCHEDULE_INTERVAL', error_if_null=True))

        self.num_connect_attempts = 10

    def get_env_bool(self, name, default_value=None, error_if_null=False):
        value = self.get_env_var(name, default_value, error_if_null)
        if value == '0':
                return False
        if value == '1':
            return True
        if type(value) == bool:
            return value
        raise KeyError(f'Boolean variable {name} returned {value}. Should be 0, 1, True, or False')

    def get_env_var(self, name, default_value=None, error_if_null=False):
        try:
            # KeyError occurs if value is not present in os
            # Because of how environment variables are passed to Docker, they will appear as '' if they are not set
            value = os.environ[name]
            if value == '':
                raise KeyError
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