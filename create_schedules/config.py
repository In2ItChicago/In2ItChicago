import os
import time
from requests.exceptions import ConnectionError

class Config:
    def __init__(self):
        self.system_username = self.get_env_var('SYSTEM_USERNAME')
        self.system_password = self.get_env_var('SYSTEM_PASSWORD')
        self.bypass_auth = self.get_env_bool('BYPASS_AUTH', False)
        
        self.scheduler_url = 'http://ndscheduler:8888/api/v1'
        self.scheduler_spider_complete = self.scheduler_url + '/spiderComplete'
        self.scheduler_jobs = self.scheduler_url + '/jobs'

        self.event_service_url = 'http://event_service:5000'

        self.cleanup_events = self.event_service_url + '/events/cleanupEvents'
        self.cleanup_scheduler = self.event_service_url + '/scheduler/cleanupScheduler'
        self.generate_schedules = self.event_service_url + '/events/generateSchedules'
        self.login = self.event_service_url + '/auth/login'
        
        self.debug = self.get_env_bool('DEBUG', False)

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

config = Config()