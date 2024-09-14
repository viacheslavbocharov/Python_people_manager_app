from datetime import datetime


class Person:
    def __init__(self, first_name, birth_date, last_name=None, middle_name=None, death_date=None, gender="M"):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.birth_date = self.validate_date(birth_date)
        self.death_date = self.validate_date(death_date) if death_date else None
        self.gender = gender

    def validate_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Дата должна быть в формате YYYY-MM-DD")

    def calculate_age(self):
        end_date = datetime.strptime(self.death_date, "%Y-%m-%d") if self.death_date else datetime.now()#получаем объект datetime
        birth_date = datetime.strptime(self.birth_date, "%Y-%m-%d")#получаем объект datetime
        age = end_date.year - birth_date.year - ((end_date.month, end_date.day) < (birth_date.month, birth_date.day))#из объекта datetime берется year & day, сравниваются кортежи, если true, то -1
        return age

    def __str__(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name or ''}".strip()
