from dadata import Dadata
import sqlite3
from os import system

db = sqlite3.connect('local_storage.db')
sql = db.cursor()

sql.execute("SELECT token, language FROM UserSettings")
data = sql.fetchall()
db.commit()


def read_token():
    for row in data:
        return row[0]


def read_language():
    for row in data:
        return row[1]


token = read_token()
language = read_language()


def print_menu():
    if language == "en":
        print('\nMENU:\n1. Language change\n2. Enter your request\n3. Exit')
    else:
        print('\nМЕНЮ:\n1. Изменить язык\n2. Ввести ваш запрос\n3. Выйти')


def find_matches():
    dadata = Dadata(token)
    if language == "en":
        query = str(input("\nEnter your geo query: "))
    else:
        query = str(input("\nВведите ваш гео-запрос: "))
    result = dadata.suggest("address", query, language=language)
    length_list = len(result)
    iterator = 0

    while iterator < length_list:
        if language == "ru":
            print("Совпадение №" + str(iterator+1))
            print(str(result[iterator]['unrestricted_value']))
        else:
            print("Matching №" + str(iterator + 1))
            print(str(result[iterator]['unrestricted_value']))
        iterator += 1

    if language == "ru":
        ultimate_number_of_query = int(input("\nВведите номер нужного совпадения: "))
        query = str(result[ultimate_number_of_query-1]['unrestricted_value'])
        ultimate_result = dadata.suggest("address", query, language=language)

        lat = ultimate_result[0]['data']['geo_lat']
        lon = ultimate_result[0]['data']['geo_lon']
        system('cls')
        print("\nШирота: " + str(lat) + "\tДолгота: " + str(lon))
    else:
        ultimate_number_of_query = int(input("\nEnter the number of match: "))
        query = str(result[ultimate_number_of_query-1]['unrestricted_value'])
        ultimate_result = dadata.suggest("address", query, language=language)

        lat = ultimate_result[0]['data']['geo_lat']
        lon = ultimate_result[0]['data']['geo_lon']
        system('cls')
        print("\nGeo-lat: " + str(lat) + "\tGeo-lon: " + str(lon))


def set_language():
    if language == "ru":
        lang = str(input("\nДоступные языки для изменения : English ('en'))+\n Введите язык: "))
        if lang != language and lang == "en":
            sql.execute(f"UPDATE UserSettings SET language = '{lang}' WHERE token = '{token}'")
            db.commit()
            print("Изменения вступят в силу после перезапуска\n")
        elif lang != language and lang != "en":
            print("\nВведите допустимое значение (en)\n")
        else:
            print("\nИзменения не требуются\n")
    else:
        lang = str(input("\nДоступные языки для изменения : Русский ('ru'))+\n Введите язык: "))
        if lang != language and lang == "ru":
            sql.execute(f"UPDATE UserSettings SET language = '{lang}' WHERE token = '{token}'")
            db.commit()
            print("\nThe changes will take effect after the restart\n")
        elif lang != language and lang != "ru":
            print("\nEnter correct lang (ru)\n")
        else:
            print("\nNo changes required\n")


def main():
    while True:
        print_menu()
        option = ''
        try:
            if language == "en":
                option = int(input('\nEnter your choice: '))
            else:
                option = int(input('\nВведите пункт меню: '))
        except:
            system('cls')
            if language == "en":
                print('\nWrong input.')
            else:
                print('\nНедопустимое значение.')

        if option == 1:
            system('cls')
            set_language()
        elif option == 2:
            system('cls')
            find_matches()
        elif option == 3:
            if language == "en":
                print('\nSee You ...')
                exit()
            else:
                print('\nЗаходите еще ...')
                exit()
        else:
            if language == "en":
                print('\nPlease enter a number from 1 to 3.')
            else:
                print('\nВведите число от 1 до 3.')


if __name__ == '__main__':
    main()
