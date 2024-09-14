import json
from person import Person


class DataManager:
    def __init__(self):
        self.persons = []

    def add_person(self, person):
        self.persons.append(person)

    def save_to_file(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump([vars(p) for p in self.persons], file, ensure_ascii=False, default=str)
            #vars() возвращает атрибуты объекта в виде словаря, это нужно для того чтобы в дальнейшем можно было
            # конвертировать в json, так как json поддерживает только(строки, числа, списки, словари)

            # json.dump() преобразует в json
            # ensure_ascii = False - символы, не являющиеся ASCII, должны оставаться как есть. Например, кириллические буквы
            #default = str задает, как обрабатывать объекты и сложные типы данных

    def load_from_file(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.persons = [Person(**p) for p in json.load(file)] #генератор списка,
                # json.load()  преобразует json в Python-структуру,
                # проходим циклом и создаем объект Person на базе итерируемых данных.
        except FileNotFoundError:
            print(f"Файл {file_name} не найден.")
        except json.JSONDecodeError:
            print("Ошибка при чтении файла данных.")

    def search_person(self, search_query):
        return [p for p in self.persons if search_query.lower() in str(p).lower()]
