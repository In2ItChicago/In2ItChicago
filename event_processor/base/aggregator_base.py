import os
import json
import re
import logging
import logging.handlers
import ptvsd

from multiprocessing import Lock
from config import config
from util.object_hash import ObjectHash
from models.event import EventManager
from datetime import datetime
from dateutil.relativedelta import relativedelta

from util.time_utils import TimeUtils
from util.http_utils import HttpUtils

class AggregatorBase:
    # This class includes functionality that should be shared by spiders and API-based classes
    enabled = True
    name = 'AggregatorBase'

    @property
    def is_errored(self):
        return any(log.levelno == logging.ERROR for log in self.memory_handler.buffer)

    def __init__(self, organization, base_url, date_format, request_date_format = None, **kwargs):
        if config.debug:
            try:
                ptvsd.enable_attach(address=('0.0.0.0', 5860))
            except:
                # attach already enabled
                pass
            if not ptvsd.is_attached():
                ptvsd.wait_for_attach()
        
        self.organization = organization
        # date_format is the string that specifies the date style of the target website
        if request_date_format == None:
            request_date_format = date_format

        self.jobid = kwargs['_job'] if '_job' in kwargs else None

        self.session = HttpUtils.get_session()

        self.date_format = date_format
        self.time_utils = TimeUtils(date_format)
        self.base_url = base_url
        self.identifier = re.sub(r'\W', '', base_url)
        self.event_manager = EventManager()

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.memory_handler = logging.handlers.MemoryHandler(0)
        self.memory_handler.setFormatter(formatter)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(formatter)

        self.configure_logger(self.name, self.memory_handler, logging.INFO)
        self.configure_logger(self.name, self.stream_handler, logging.INFO)
        self.configure_logger('scrapy', self.memory_handler, logging.WARNING)
        self.configure_logger('scrapy', self.stream_handler, logging.WARNING)
        self.configure_logger('twisted', self.memory_handler, logging.WARNING)
        self.configure_logger('twisted', self.stream_handler, logging.WARNING)
        
        start_date = datetime.now().strftime('%m-%d-%Y')
        end_date = (datetime.now() + relativedelta(months=+1)).strftime('%m-%d-%Y')
        
        request_format_utils = TimeUtils('%m-%d-%Y')
        # When this is running for multiple days, validating if the date is in the past causes issues
        self.start_date = request_format_utils.convert_date_format(start_date, request_date_format, validate_past=False)
        self.end_date = request_format_utils.convert_date_format(end_date, request_date_format, validate_past=False)
        self.start_timestamp = request_format_utils.min_timestamp_for_day(start_date)
        self.end_timestamp = request_format_utils.max_timestamp_for_day(end_date)

    def configure_logger(self, logger, handler, log_level):
        logging.getLogger(logger).addHandler(handler)
        logging.getLogger(logger).setLevel(log_level)

    def notify_spider_complete(self):
        logs = [self.memory_handler.format(log) for log in self.memory_handler.buffer]
        return session.post(config.scheduler_spider_complete, 
                            json={'jobid': self.jobid, 'errored': self.is_errored, 'logs': logs}, 
                            headers={'Content-Type': 'application/json'})