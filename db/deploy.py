from sqlbag import S, create_database, drop_database
from migra import Migration
from contextlib import contextmanager
import glob

def get_sql(file):
    with open(file, 'r') as f:
        return f.read()

def run_all(folder, s_target):
    for filename in glob.iglob(f'{folder}/**/*.sql', recursive=True):
        s_target.execute(get_sql(filename))

@contextmanager
def temp_db(url):
    try:
        create_database(url)
        yield url
    finally:
        drop_database(url)



def sync():
    DB_URL = 'postgresql://postgres:postgres@localhost:5432/scheduler'
    with temp_db('postgresql://postgres:postgres@localhost:5432/temp') as TEMP_DB_URL:
        create_database(TEMP_DB_URL)
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
                if input('Apply these changes? (y/n)') == 'y':
                    print('Applying...')
                    m.apply()
                else:
                    print('Not applying.')
            else:
                print('Already synced.')
sync()