import os
import sys
import time
import requests

class Config:
    def __init__(self, local_db_client=False):
        self.local_db_client = local_db_client

        self.db_client_ip = self.get_client_ip()
        self.db_client_port = 5000
        self.db_client_url = f'http://{self.db_client_ip}:{self.db_client_port}'

        self.db_get_events = self.db_client_url + '/getevents'
        self.db_put_events = self.db_client_url + '/putevents'
        self.db_client_status = self.db_client_url + '/status'
        
        self.docker_ip = self.get_env_var('DOCKER_IP')

        self.db_ip = 'clipboard_db' if self.db_client_ip == 'clipboard_db_client' else self.docker_ip
        self.db_port = 27017
        self.db_url = f'mongodb://{self.db_ip}:{self.db_port}/clipboard'
        
        self.num_connect_attempts = 10

        self.display_date_format = '%Y-%m-%d'
        self.display_time_format = '%H:%M'

    def get_env_var(self, name):
        try:
            return os.environ[name]
        except KeyError:
            raise KeyError(f'Error: environment variable {name} not set. If this value was recently set, close all python processes and try again')

    def get_client_ip(self):
        if self.local_db_client:
                return 'localhost'
        elif self.get_env_var('DB_CLIENT_IP') == 'clipboard_db_client':
            # data engine is running in Docker
            return 'clipboard_db_client'
        else:
            # db client is running in Docker but data engine is not
            return self.get_env_var('DOCKER_IP')
    
    def connect_to_client(self):
        for _ in range(self.num_connect_attempts):
            try:
                requests.get(self.db_client_url + '/status')
                print('Connection successful')
                return True, 'Connection successful'
            except requests.exceptions.ConnectionError:
                time.sleep(0.5)
                continue

        return False, 'Connection to db client failed. Make sure the service is running and the url is set correctly.'
        