from sqlbag import S, create_database, drop_database
from migra import Migration
from contextlib import contextmanager
import glob
from queue import SimpleQueue
from sqlalchemy.exc import ProgrammingError

def get_sql(file):
    with open(file, 'r') as f:
        return f.read()

def run_all(folder, s_target):
    sql_queue = SimpleQueue()
    size = 0
    for filename in glob.iglob(f'{folder}/**/*.sql', recursive=True):
        sql_queue.put(get_sql(filename))
        size += 1
    while not sql_queue.empty():
        try:
            sql = sql_queue.get()
            s_target.execute(sql)
            s_target.commit()
        except ProgrammingError as e:
            message = str(e.orig).strip()
            if 'relation' in message and 'does not exist' in message:
                s_target.rollback()
                print(f'Object does not exist yet: {message}. Re-queueing...')
                sql_queue.put(sql)
            else:
                raise

@contextmanager
def temp_db(url):
    try:
        create_database(url)
        yield url
    finally:
        drop_database(url)



def sync():
    DB_URL = 'postgresql://postgres:postgres@postgres:5432/scheduler'
    with temp_db('postgresql://postgres:postgres@postgres:5432/temp') as TEMP_DB_URL:
        create_database(TEMP_DB_URL)
        create_database(DB_URL)
        with S(DB_URL) as s_current, S(TEMP_DB_URL) as s_target:
            run_all('schemas', s_target)
            run_all('tables', s_target)
            m = Migration(s_current, s_target)
            m.set_safety(False)
            m.add_all_changes()

            if m.statements:
                print('THE FOLLOWING CHANGES ARE PENDING:', end='\n\n')
                print(m.sql)
                print()
                if input('Apply these changes? (y/n) ') == 'y':
                    print('Applying...')
                    m.apply()
                else:
                    print('Not applying.')
            else:
                print('Already synced.')
sync()