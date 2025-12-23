import sqlite3

def test():
    try:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        print("коннект есть")
    except Exception as e:
        print("коннекта нет")
        return 0
    
    cursor.execute("select name from sqlite_master where type='table'")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    executed_tables = ['aboba', 'abobi']

    for table in executed_tables:
        if table in table_names:
            print(f'таблица {table} есть')
        else:
            print(f'таблицы {table} нет')
    conn.close()


def debug():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    print("первые три значения:")

    cursor.execute('''
select aa.aboba_name, ai.abobi_name, ai.aboba_id
from aboba aa
join abobi ai on aa.aboba_id = ai.aboba_id
limit 3''')
    
    for row in cursor.fetchall():
        aboba_name, abobi_name, aboba_id = row
    
    conn.close()
        