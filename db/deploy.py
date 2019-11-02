from sqlbag import S, create_database, drop_database
from migra import Migration
from contextlib import contextmanager
import glob
from queue import SimpleQueue
from sqlalchemy.exc import ProgrammingError, OperationalError
import sys
import time
import os

databases = ['events', 'scheduler']
sync_attempts = 100

def get_sql(file):
    with open(file, 'r') as f:
        return f.read()

def run_all(folder, s_target):
    sql_queue = SimpleQueue()
    size = 0
    for filename in glob.iglob(f'{folder}/**/*.sql', recursive=True):
        sql_queue.put(get_sql(filename))
        size += 1
    num_tries = 0
    max_tries = size * 2
    while not sql_queue.empty() and num_tries < max_tries:
        try:
            sql = sql_queue.get()
            s_target.execute(sql)
            s_target.commit()
            num_tries = 0
        except ProgrammingError as e:
            message = str(e.orig).strip()
            if 'relation' in message and 'does not exist' in message:
                s_target.rollback()
                print(f'Object does not exist yet: {message}. Re-queueing...')
                sql_queue.put(sql)
                num_tries += 1
            else:
                raise
    if num_tries >= max_tries:
        print(f'Number of attempts exceeded configured threshold of {max_tries}')
        sys.exit(1)

@contextmanager
def temp_db(url):
    try:
        # Drop if exists in case the previous deployment didn't clean up for some reason
        create_database(url, wipe_if_existing=True)
        yield url
    finally:
        drop_database(url)

def sync(database):
    if os.getenv('HOSTINGENV') == 'DEV':
        db_url_format = 'postgresql://postgres:postgres@postgres:5432/%s' 
    else:
        db_url_format = 'postgresql://postgres:postgres@/%s?host=/var/run/postgresql' 
    temp_db_url = db_url_format % f'{database}temp'
    db_url = db_url_format % database
    with temp_db(temp_db_url) as s_target_temp:
        create_database(db_url)
        with S(db_url) as s_current, S(s_target_temp) as s_target:
            run_all(f'{database}/schemas', s_target)
            run_all(f'{database}/tables', s_target)
            m = Migration(s_current, s_target)
            m.set_safety(False)
            m.add_all_changes()

            if m.statements:
                print('THE FOLLOWING CHANGES ARE PENDING:', end='\n\n')
                print(m.sql)
                print()
                if (len(sys.argv) > 1 and sys.argv[1] == 'noconfirm') or input('Apply these changes? (y/n) ') == 'y':
                    print('Applying...')
                    m.apply()
                else:
                    print('Not applying.')
            else:
                print('Already synced.')

def try_sync(database):
    # Wait for the database to become operational
    for i in range(sync_attempts):
        try:
            sync(database)
            break
        except OperationalError as e:
            if i == sync_attempts - 1:
                raise e
            continue

for database in databases: 
    print(f'Syncing {database}...')
    try_sync(database)