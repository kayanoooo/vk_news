import sqlite3

def report(aboba, abobi):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    with open('report.txt', 'w', encoding='utf-8') as f:
        f.write('первые два значения')

        cursor.execute('''
    select aa.aboba_name, ai.abobi_name, ai.aboba_id
    from aboba aa
    join abobi ai on aa.aboba_id = ai.aboba_id
    limit 2''')
        
        for row in cursor.fetchall():
            aboba_name, abobi_name, aboba_id = row
            f.write(f'{aboba_name}, {abobi_name}, {aboba_id}')

        print("отчёт создался")

    conn.close()
    
