import functools
import logging
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from util.switchable_decorator import SwitchableDecorator
from config import config

cache = CacheManager(**parse_cache_config_options({
        'cache.type': 'file',
        'cache.data_dir': '/tmp/beaker/data',
        'cache.lock_dir': '/tmp/beaker/lock'
    }))

def try_cache(target):
    def try_call(*args, **kwargs):
        try:
            return cache.cache('web_call', expire=config.api_cache_expiration)(target)(*args, **kwargs)
        except Exception as e:
            logging.getLogger('scrapy').warning('Exception while calling cache: ' + str(e))
        return target(*args, **kwargs)
    return try_call
    
cache_call = SwitchableDecorator(try_cache, config.enable_api_cache)