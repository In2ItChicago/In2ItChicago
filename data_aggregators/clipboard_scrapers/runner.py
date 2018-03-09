from scrapy.cmdline import execute
import os
try:
    os.chdir('data_aggregators')
    execute(['scrapy', 'crawl', 'history', '-a', 'start_date=20180304', '-a', 'end_date=20180420'])
except SystemExit as se:
    if se.code == 0:
        print("success")
    else:
        print("error")