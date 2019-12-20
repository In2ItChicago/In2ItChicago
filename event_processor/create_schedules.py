import math
import time
from scrapy import spiderloader
from scrapy.utils import project
from event_processor.config import config
from jobs import jobs
from requests.exceptions import ConnectionError
from event_processor.util.http_utils import HttpUtils

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
    
    @classmethod
    def from_interval(cls, name, job_class, interval, delta, offset, args):
        current_offset = int(delta * offset)
        if interval >= MINUTES_IN_HOUR:
            minute = current_offset % MINUTES_IN_HOUR
            hour = f'{current_offset // MINUTES_IN_HOUR}-{HOURS_IN_DAY - 1}/{interval // MINUTES_IN_HOUR}'
        else:
            minute = f'{current_offset}-{MINUTES_IN_HOUR - 1}/{interval}'
            hour = '*'
        return cls(name, job_class, minute, hour, args)

class ScheduleBuilder:
    def __init__(self):
        self.session = HttpUtils.get_session(convert_snake_case=False)
        for _ in range(ATTEMPTS):
            try:
                scrapy_jobs = self.session.get(config.scheduler_jobs)
                break
            except ConnectionError:
                time.sleep(5)
        jobs_json = scrapy_jobs.json()
        self.jobs_dict = {job['name']: job for job in jobs_json['jobs']}
    
    def add_schedules(self):
        self.add_spider_schedules()
        self.add_other_schedules()
    
    def add_spider_schedules(self):
        settings = project.get_project_settings()
        spider_loader = spiderloader.SpiderLoader.from_settings(settings)
        spiders = spider_loader.list()
        classes = [s for s in (spider_loader.load(name) for name in spiders) if s.enabled]

        delta = math.ceil(config.schedule_interval / len(classes))

        schedules = [Schedule.from_interval(scraper.name, SPIDER_CLASS, config.schedule_interval, delta, index, [scraper.name]) for index, scraper in enumerate(classes)]

        for schedule in schedules:
            self.add_schedule(schedule)
    
    def add_other_schedules(self):
        for job in jobs:
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
            response = self.session.put(f'{config.scheduler_jobs}/{job["job_id"]}', json=json_payload)
            if response.ok:
                print(f'Updated schedule for {schedule.name}')
            else:
                raise Exception(response.text)
        else:
            response = self.session.post(config.scheduler_jobs, json=json_payload)
            if response.ok:
                print(f'Added schedule for {schedule.name}')
            else:
                raise Exception(response.text)

if __name__ == '__main__':
    if config.debug:
        import ptvsd
        ptvsd.enable_attach(address=('0.0.0.0', 5860))
        ptvsd.wait_for_attach()
        
    builder = ScheduleBuilder()
    builder.add_schedules()