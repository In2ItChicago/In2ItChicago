def sync():
    from sqlbag import S, temporary_database as temporary_db
    from migra import Migration

    DB_URL = 'postgresql://postgres:postgres@localhost:5432/test'
    TEMP_DB_URL = 'postgresql://postgres:postgres@localhost:5432/test2'
    with S(DB_URL) as s_current, S(TEMP_DB_URL) as s_target:
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