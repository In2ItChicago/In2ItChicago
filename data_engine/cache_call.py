import functools
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from switchable_decorator import SwitchableDecorator
from config import API_DELAY_SECONDS, API_CACHE_EXPIRATION, ENABLE_API_CACHE

cache = CacheManager(**parse_cache_config_options({
        'cache.type': 'file',
        'cache.data_dir': 'data',
        'cache.lock_dir': 'lock'
    }))

cache_call = SwitchableDecorator(cache.cache('web_call', expire=API_CACHE_EXPIRATION), ENABLE_API_CACHE)