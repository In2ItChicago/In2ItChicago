from event_processor.config import config

CURL_CLASS = 'simple_scheduler.jobs.curl_job.CurlJob'

jobs = [
    {
        'name': 'cleanupData',
        'job_class': CURL_CLASS,
        'hour': 0,
        'minute': 0,
        'args': [config.cleanup_events,'DELETE']
    },
    {
        'name': 'cleanupScheduler',
        'job_class': CURL_CLASS,
        'hour': 0,
        'minute': 15,
        'args': [config.cleanup_scheduler,'DELETE']
    }
]