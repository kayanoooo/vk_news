import sqlite3
from aboba import Aboba
from abobi import Abobi

def load_all():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    aboba, abobi = [], []

    cursor.execute('select aboba_id, aboba_name from aboba order by aboba_id')
    for row in cursor.fetchall():
        aboba.append(Aboba(row[0], row[1]))

    cursor.execute('select abobi_id, abobi_name, aboba_id from abobi order by abobi_id')
    for row in cursor.fetchall():
        abobi.append(Abobi(row[0], row[1], row[2]))

    conn.close()

    print(f'загружены {len(aboba)} строк из aboba и {len(abobi)} из abobi')

    return aboba, abobi