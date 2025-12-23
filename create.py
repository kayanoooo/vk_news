import sqlite3

def create_db():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute('''
create table aboba (
    aboba_id integer primary key,
    aboba_name text)''')

    cursor.execute('''
create table abobi (
    abobi_id integer primary key,
    abobi_name text,
    aboba_id integer,
    foreign key (aboba_id) references aboba(aboba_id))''')

    aboba = [
        (1, 'lg'),
        (2, 'samsung'),
        (3, 'htc'),
        (4, 'apple')
    ]

    abobi = [
        (1, 'g5', 1),
        (2, 'galaxy s1', 2),
        (3, 'one', 3),
        (4, 'iphone 4', 4)
    ]

    cursor.executemany('insert into aboba (aboba_id, aboba_name) values (?, ?)', aboba)
    cursor.executemany('insert into abobi (abobi_id, abobi_name, aboba_id) values (?, ?, ?)', abobi)

    conn.commit()
    conn.close()

    print('база данных создана')
