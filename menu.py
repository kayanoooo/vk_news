import sqlite3
from create import create_db
from data import load_all
from test_debug import test, debug
from reports import report

def show_menu():
    print('1. загрузка данных')
    print('2. создать бд')
    print('3. сделать тест')
    print('4. показать отладку')
    print('5. создать отчёт')
    print('6. показать сложность')
    print('7. выйти')

def big_o():
    print('везде O(n)')


def main():
    show_menu()
    aboba, abobi = [], []

    while True:
        choice = input("выберите: ")
        if choice == '1':
            aboba, abobi = load_all()
        elif choice == '2':
            create_db()
        elif choice == '3':
            test()
        elif choice == '4':
            debug()
        elif choice == '5':
            report(aboba, abobi)
        elif choice == '6':
            big_o()
        elif choice == '7':
            break
        else:
            print('выберите другое число')
