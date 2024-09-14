import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter import ttk
from dateutil import parser
from data_manager import DataManager
from person import Person


class PeopleApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("People Manager")
        self.geometry("750x400+0+0")
        self.data_manager = DataManager()

        # Создание фрейма для кнопок меню в верхней части окна
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Button(button_frame, text="Загрузить данные из файла", command=self.load_data).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Сохранить данные в файл", command=self.save_data).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Добавить нового человека", command=self.add_person).pack(side=tk.LEFT, padx=5)

        # Кнопка "Найти", которая будет меняться на "Сбросить"
        self.search_button = tk.Button(button_frame, text="Найти", command=self.search_or_reset)
        self.search_button.pack(side=tk.RIGHT, padx=5)

        # Поле для ввода поискового запроса
        self.search_entry = tk.Entry(button_frame)
        self.search_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)

        # tk.Button(button_frame, text="Выход", command=self.quit).pack(side=tk.LEFT, padx=5)

        # Создание фрейма для таблицы с данными о людях
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Создание Treeview для отображения данных в виде таблицы
        self.tree = ttk.Treeview(self.frame, columns=("ФИО", "Дата рождения", "Дата смерти", "Полных лет", "Пол"),
                                 show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Определение заголовков столбцов
        self.tree.heading("ФИО", text="ФИО")
        self.tree.heading("Дата рождения", text="Дата рождения")
        self.tree.heading("Дата смерти", text="Дата смерти")
        self.tree.heading("Полных лет", text="Полных лет")
        self.tree.heading("Пол", text="Пол")

        # Определение ширины столбцов
        self.tree.column("ФИО", width=200)
        self.tree.column("Дата рождения", width=100)
        self.tree.column("Дата смерти", width=150)
        self.tree.column("Полных лет", width=80)
        self.tree.column("Пол", width=80)

        # Добавляем прокрутку для таблицы
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Проверка и обновление списка при запуске
        self.update_table()

    def parse_date(self, date_str):
        """Парсинг даты и преобразование её в формат YYYY-MM-DD."""
        try:
            parsed_date = parser.parse(date_str,
                                       dayfirst=True)  # Используем dayfirst=True, чтобы правильно обрабатывать форматы с первым днем, возвращ объект datetime
            return parsed_date.strftime("%Y-%m-%d") #преобразовует datetime в строку
        except ValueError:
            raise ValueError(
                "Некорректный формат даты. Используйте форматы: 'DD.MM.YYYY', 'DD MM YYYY', 'DD/MM/YYYY', 'D-M-YYYY' и т.п.")

    def format_date(self, date_str):
        """Преобразование даты из формата YYYY-MM-DD в формат DD.MM.YYYY."""
        if date_str:
            parsed_date = parser.parse(date_str)
            return parsed_date.strftime("%d.%m.%Y")
        return None

    def update_table(self, persons=None):
        """Обновление содержимого таблицы с данными о людях."""
        for row in self.tree.get_children():
            self.tree.delete(row)  # Очистка таблицы

        persons = persons if persons is not None else self.data_manager.persons
        if not persons:
            self.tree.insert("", tk.END, values=("Нет данных", "", "", "", ""))
        else:
            for person in persons:
                fio = f"{person.first_name} {person.middle_name or ''} {person.last_name or ''}".strip()
                # fio = person.__str__()
                birth_date = self.format_date(person.birth_date)

                if person.death_date:
                    death_date = self.format_date(person.death_date)
                    death_display = f"Умер {death_date}" if person.gender == 'M' else f"Умерла {death_date}"
                else:
                    death_display = "Нет"

                age = person.calculate_age()  # Вычисляем количество полных лет

                gender_display = "Мужчина" if person.gender == 'M' else "Женщина"  # Преобразуем M/F в Мужчина/Женщина

                self.tree.insert("", tk.END, values=(fio, birth_date, death_display, age, gender_display))

    def add_person(self):
        """Добавление нового человека."""
        first_name = simpledialog.askstring("Имя", "Введите имя:")
        if not first_name:
            messagebox.showerror("Ошибка", "Имя является обязательным полем.")
            return

        last_name = simpledialog.askstring("Фамилия", "Введите фамилию (необязательно):")
        middle_name = simpledialog.askstring("Отчество", "Введите отчество (необязательно):")
        birth_date_str = simpledialog.askstring("Дата рождения",
                                                "Введите дату рождения (DD.MM.YYYY, DD MM YYYY, DD/MM/YYYY, D-M-YYYY):")
        death_date_str = simpledialog.askstring("Дата смерти",
                                                "Введите дату смерти (если есть, DD.MM.YYYY, DD MM YYYY, DD/MM/YYYY, D-M-YYYY):")

        # Выпадающий список для выбора пола
        gender = self.select_gender()
        if not gender:
            messagebox.showerror("Ошибка", "Пол является обязательным полем.")
            return

        try:
            birth_date = self.parse_date(birth_date_str)  # Парсим дату рождения
            death_date = self.parse_date(
                death_date_str) if death_date_str else None  # Парсим дату смерти, если она есть

            person = Person(first_name, birth_date, last_name, middle_name, death_date, gender)
            self.data_manager.add_person(person)
            messagebox.showinfo("Успех", "Человек успешно добавлен!")
            self.update_table()  # Обновляем таблицу после добавления нового человека
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")

    def select_gender(self):
        """Окно с выпадающим списком для выбора пола."""
        gender_selection = tk.Toplevel(self)
        gender_selection.title("Выбор пола")

        tk.Label(gender_selection, text="Выберите пол:").pack(pady=10)

        gender_var = tk.StringVar()
        gender_combobox = ttk.Combobox(gender_selection, textvariable=gender_var, state="readonly")
        gender_combobox['values'] = ("Мужчина", "Женщина")
        gender_combobox.pack(pady=10)

        def on_select():
            selected_gender = gender_combobox.get()
            if selected_gender == "Мужчина":
                gender_var.set("M")
            elif selected_gender == "Женщина":
                gender_var.set("F")
            gender_selection.destroy()

        tk.Button(gender_selection, text="ОК", command=on_select).pack(pady=10)

        self.wait_window(gender_selection)
        return gender_var.get()

    def search_or_reset(self):
        """Поиск человека или сброс списка в зависимости от состояния кнопки."""
        if self.search_button.cget("text") == "Найти":
            search_query = self.search_entry.get()
            if search_query:
                results = self.data_manager.search_person(search_query)
                self.update_table(results)  # Обновляем таблицу найденными людьми
                self.search_button.config(text="Сбросить")
            else:
                messagebox.showinfo("Поиск", "Введите строку для поиска.")
        else:
            self.search_entry.delete(0, tk.END)  # Очищаем поле ввода
            self.update_table()  # Возвращаем таблицу всех людей
            self.search_button.config(text="Найти")

    def load_data(self):
        """Загрузка данных из файла."""
        file_name = filedialog.askopenfilename(title="Выберите файл для загрузки", filetypes=[("JSON files", "*.json")])
        if file_name:
            self.data_manager.load_from_file(file_name)
            # messagebox.showinfo("Успех", "Данные успешно загружены!")
            self.update_table()  # Обновляем таблицу после загрузки данных

    def save_data(self):
        """Сохранение данных в файл."""
        file_name = filedialog.asksaveasfilename(title="Сохранить файл", defaultextension=".json",#filedialog из tkinter
                                                 filetypes=[("JSON files", "*.json")])#в file_name записана строка с полным путем к файлу
        if file_name:
            self.data_manager.save_to_file(file_name)
            messagebox.showinfo("Успех", "Данные успешно сохранены!")


if __name__ == "__main__":
    app = PeopleApp()
    app.mainloop()

