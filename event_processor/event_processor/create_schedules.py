import math
import time
from scrapy import spiderloader
from scrapy.utils import project
from event_processor.config import config
from requests.exceptions import ConnectionError
import ptvsd
from event_processor.util.http_utils import HttpUtils

HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
JOB_CLASS = 'simple_scheduler.jobs.scrapy_job.ScrapyJob'
ATTEMPTS = 100

class Schedule:
    """Represents a schedule for (running a spider?)"""
    def __init__(self, name, interval, delta, offset):
        self.name = name
        current_offset = int(delta * offset)
        if interval >= MINUTES_IN_HOUR:
            self.minute = current_offset % MINUTES_IN_HOUR
            self.hour = f'{current_offset // MINUTES_IN_HOUR}-{HOURS_IN_DAY - 1}/{interval // MINUTES_IN_HOUR}'
        else:
            self.minute = f'{current_offset}-{MINUTES_IN_HOUR - 1}/{interval}'
            self.hour = '*'

def run():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    classes = [s for s in (spider_loader.load(name) for name in spiders) if s.enabled]

    session = HttpUtils.get_session(convert_snake_case=False)
    for _ in range(ATTEMPTS):
        try:
            scrapy_jobs = session.get(config.scheduler_jobs)
            break
        except ConnectionError:
            time.sleep(5)
    jobs_json = scrapy_jobs.json()
    jobs_dict = {job['name']: job for job in jobs_json['jobs'] if job['job_class_string'] == JOB_CLASS}

    delta = math.ceil(config.schedule_interval / len(classes))

    schedules = [Schedule(scraper.name, config.schedule_interval, delta, index) for index, scraper in enumerate(classes)]

    for schedule in schedules:
        json_payload = {
                'hour': schedule.hour, 
                'minute': schedule.minute, 
                'name': schedule.name,
                'job_class_string': JOB_CLASS,
                'pub_args': [schedule.name]
            }
        if schedule.name in jobs_dict:
            job = jobs_dict[schedule.name]
            response = session.put(f'{config.scheduler_jobs}/{job["job_id"]}', json=json_payload)
            if response.ok:
                print(f'Updated schedule for {schedule.name}')
            else:
                raise Exception(response.text)
        else:
            response = session.post(config.scheduler_jobs, json=json_payload)
            if response.ok:
                print(f'Added schedule for {schedule.name}')
            else:
                raise Exception(response.text)

if __name__ == '__main__':
    if config.debug:
        ptvsd.enable_attach(address=('0.0.0.0', 5860)) #todo: put this in a config file? 
        ptvsd.wait_for_attach()
        
    run()