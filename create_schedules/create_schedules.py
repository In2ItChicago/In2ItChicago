import math
import time
import requests
from config import config
from jobs import get_jobs
from requests.exceptions import ConnectionError

HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
SPIDER_CLASS = 'simple_scheduler.jobs.scrapy_job.ScrapyJob'
CURL_CLASS = 'simple_scheduler.jobs.curl_job.CurlJob'
ATTEMPTS = 100

class Schedule:

    def __init__(self, name, job_class, minute, hour, args):
        self.name = name
        self.job_class = job_class
        self.minute = minute
        self.hour = hour
        self.args = args

class ScheduleBuilder:
    def __init__(self):
        for _ in range(ATTEMPTS):
            try:
                scrapy_jobs = requests.get(config.scheduler_jobs)
                break
            except ConnectionError:
                time.sleep(5)
        jobs_json = scrapy_jobs.json()
        self.jobs_dict = {job['name']: job for job in jobs_json['jobs']}
    
    def add_schedules(self):
        for job in get_jobs():
            self.add_schedule(Schedule(job['name'], job['job_class'], job['minute'], job['hour'], job['args']))

    def add_schedule(self, schedule):
        json_payload = {
                    'hour': schedule.hour, 
                    'minute': schedule.minute, 
                    'name': schedule.name,
                    'job_class_string': schedule.job_class,
                    'pub_args': schedule.args
                }
        if schedule.name in self.jobs_dict:
            job = self.jobs_dict[schedule.name]
            response = requests.put(f'{config.scheduler_jobs}/{job["job_id"]}', json=json_payload)
            if response.ok:
                print(f'Updated schedule for {schedule.name}')
            else:
                raise Exception(response.text)
        else:
            response = requests.post(config.scheduler_jobs, json=json_payload)
            if response.ok:
                print(f'Added schedule for {schedule.name}')
            else:
                raise Exception(response.text)

if __name__ == '__main__':
    # if config.debug:
    #     import ptvsd
    #     ptvsd.enable_attach(address=('0.0.0.0', 5860))
    #     ptvsd.wait_for_attach()
        
    builder = ScheduleBuilder()
    builder.add_schedules()