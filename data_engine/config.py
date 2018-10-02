from clipboardcommonlib import shared_config

ENABLE_API_CACHE = True
API_CACHE_EXPIRATION = 3600
API_DELAY_SECONDS = .1

ENABLE_SCRAPY_CACHE = True
SCRAPY_CACHE_EXPIRATION = 3600
VERBOSE_SCRAPY_OUTPUT = False

config = shared_config.Config()
# import os
# import sys
# class Config:
#     db_client_ip = ''

#     @staticmethod
#     def initialize():
#         Config.set_client_ip()

#     @staticmethod
#     def get_env_var(name):
#         try:
#             return os.environ[name]
#         except KeyError:
#             print(f'Error: {name} not set. If this value was recently set, close all python processes and try again')
#             sys.exit(1)

#     @staticmethod
#     def set_client_ip():
#         if LOCAL_DB_CLIENT:
#             Config.db_client_ip = 'localhost'
#         elif Config.get_env_var('DB_CLIENT_IP') == '0.0.0.0':
#             # data engine is running in Docker
#             Config.db_client_ip = 'clipboard_db_client'
#         else:
#             # db client is running in Docker but data engine is not
#             Config.db_client_ip = Config.get_env_var('DOCKER_IP')
