import functools
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from switchable_decorator import SwitchableDecorator
from config import config

cache = CacheManager(**parse_cache_config_options({
        'cache.type': 'file',
        'cache.data_dir': '/tmp/beaker/data',
        'cache.lock_dir': '/tmp/beaker/lock'
    }))

cache_call = SwitchableDecorator(cache.cache('web_call', expire=config.api_cache_expiration), config.enable_api_cache)