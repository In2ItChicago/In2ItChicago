from config import config

CURL_CLASS = 'simple_scheduler.jobs.curl_job.CurlJob'

def get_jobs():
    system_username = None if config.bypass_auth else config.system_username
    system_password = None if config.bypass_auth else config.system_password
    # Note: time is in UTC
    return [
        {
            'name': 'cleanupData',
            'job_class': CURL_CLASS,
            'hour': 6,
            'minute': 0,
            'args': [config.cleanup_events,'DELETE', system_username, system_password, config.login]
        },
        {
            'name': 'cleanupScheduler',
            'job_class': CURL_CLASS,
            'hour': 6,
            'minute': 15,
            'args': [config.cleanup_scheduler,'DELETE', system_username, system_password, config.login]
        },
        {
            'name': 'generateSchedules',
            'job_class': CURL_CLASS,
            'hour': 6,
            'minute': 30,
            'args': [config.generate_schedules,'POST', system_username, system_password, config.login]
        }
    ]