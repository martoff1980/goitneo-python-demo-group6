import json
import datetime
import re
from collections import UserDict
from colorama import init, Fore, Style
init()

class Address:
    def __init__(self, address):
        if len(address) <= 120:
            self.addresses = [address]
        else:
            raise ValueError("\nАдреса перевищує максимально допустиму довжину в 120 символів.")

    def add_address(self, address):
        if isinstance(address, str):
            self.addresses.append(address)
        else:
            print("\nНедійсний формат адреси. Укажіть рядок.")

    def show_address(self, name):
        if self.addresses:
            return f"\nАдреса для контакту {name}: {self.addresses[0]}"
        else:
            return "Адреса не була вказана."
            
    def edit_address(self, new_address):
        self.addresses = [new_address]
        return "Адресу успішно відредаговано."

    def delete_address(self, address):
        self.addresses = [a for a in self.addresses if str(a) != str(address)]

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, first_name, last_name=None):
        if last_name:
            super().__init__(f"{first_name} {last_name}")
        else:
            super().__init__(first_name)

class Phone(Field):
    def __init__(self, value):
        if self._validate_phone(value):
            super().__init__(value)
        else:
            raise ValueError("\nНеправильний формат номеру телефону. Номер повинен містити 10 цифр.")

    def _validate_phone(self,value):
        return len(value) == 10 and value.isdigit()

class Email(Field):
    def __init__(self, value):
        self.pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if self.pattern.match(value):
            self.value = value
        else:
            raise ValueError("Неіснуючий формат адреси електронної пошти.\nПовторіть спробу.")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Неправильний формат дати народження. Використовуйте формат ДД.ММ.РРРР.")

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')



class Notion:
    def __init__(self, text, hashtags):
        self.text = self._validate_text(text)
        self.hashtags = self._validate_hashtags(hashtags)

    def _validate_text(self, text):
        if not text or len(text) > 280:
            raise ValueError("Текст нотатки не може бути порожнім або перевищувати 280 символів.")
        return text

    @staticmethod
    def _validate_hashtags(hashtags):
        validated_hashtags = []
        pattern = re.compile(r"^#\w+$")
        for hashtag in hashtags:
            if pattern.match(hashtag):
                validated_hashtags.append(hashtag)
            else:
                raise ValueError("Неправильний формат хештегу.")
        return validated_hashtags
    
def get_valid_hashtags():
    while True:
        hashtags_input = input("Додайте хештеги: ")
        hashtags = hashtags_input.split()
        try:
            validated_hashtags = Notion._validate_hashtags(hashtags)
            return validated_hashtags
        except ValueError as e:
            print(e)
            print("Будь ласка, спробуйте ввести хештеги ще раз.")

class Find:
    @staticmethod
    def find_by_name(address_book, name):
        found_contacts = []
        for record in address_book.values():
            if record.name.value.lower() == name.lower():
                found_contacts.append(record)
        return found_contacts

    @staticmethod
    def find_by_phone(address_book, phone):
        found_contacts = []
        for record in address_book.values():
            for record_phone in record.phones:
                if str(record_phone) == phone:
                    found_contacts.append(record)
                    break
        return found_contacts

    @staticmethod
    def find_by_birthday(address_book, birthday):
        found_contacts = []
        for record in address_book.values():
            if record.birthday and str(record.birthday) == birthday:
                found_contacts.append(record)
        return found_contacts
    
    @staticmethod
    def find_by_address(address_book, address):
        found_contacts = []
        for record in address_book.values():
            if record.address and address in record.address.addresses:
                found_contacts.append(record)
        return found_contacts

    @staticmethod
    def find_by_email(address_book, email):
        found_contacts = []
        for record in address_book.values():
            if record.email and record.email.value.lower() == email.lower():
                found_contacts.append(record)
        return found_contacts


class Record:
    def __init__(self, name):
        self.original_name = name
        self.name = Name(*name.split())
        self.phones = []
        self.email = None
        self.birthday = None
        self.notions = []
        self.address = None
        self.data = {}

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(e)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone_index, new_phone):
        try:
            old_phone_index = int(old_phone_index)
            if 0 <= old_phone_index < len(self.phones):
                self.phones[old_phone_index] = Phone(new_phone)
                return "\nНомер телефону успішно змінено."
            else:
                print("\nНевірний індекс номеру телефону.")
        except ValueError:
            print("\nНевірний індекс номеру телефону. Будь ласка, введіть коректний номер.")

    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    def delete(self, name):
        pass

    def display_phones(self):
        for i, phone in enumerate(self.phones):
            print(f"{i}: {phone}")


    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def add_email(self, email):
        self.email = Email(email)

    def show_email(self):
        if self.email:
            return str(self.email)
        else:
            return "не додана"

    def edit_email(self, new_email):
        if self.email is not None:
            self.email = Email(new_email)
        else:
            self.add_email(new_email)

    def delete_email(self, email_address):
        if self.email is not None:
            if self.email.value == email_address:
                self.email = None
                print("Електронну пошту успішно видалено!")
            else:
                print("Електронна пошта не знайдена.")
        else:
            print("Контакт не має електронної пошти для видалення.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return str(self.birthday)
        else:
            return "не додано"
    
    def add_notion(self, text, hashtags):
        hashtag_list = hashtags
        self.notions.append(Notion(text, hashtags))

    def edit_notion(self, index, new_text, new_hashtags):
        try:
            index = int(index)
            if 0 <= index < len(self.notions):
                self.notions[index] = Notion(new_text, new_hashtags)
                return "Нотатку успішно змінено."
            else:
                return "Неправильний індекс нотатки."
        except ValueError as e:
            print(e)

    def delete_notion(self, index):
        try:
            index = int(index)
            if 0 <= index < len(self.notions):
                del self.notions[index]
                return "Нотатку успішно видалено."
            else:
                print("Неправильний індекс нотатки.")
        except ValueError as e:
            print(e)

    def __str__(self):
        phones_str = '; '.join([str(phone) for phone in self.phones])
        birthday_str = self.show_birthday() if self.birthday else "не додано"
        notions_str = '; '.join([f"{notion.text} (Хештеги: {' '.join(notion.hashtags)})" for notion in self.notions])
        address_str = ', '.join(self.address.addresses) if hasattr(self, 'address') and self.address else "не додана"
        return f"Ім'я контакту: {self.original_name}, Телефони: {phones_str}, Електронна пошта: {self.show_email()}, День народження: {birthday_str}, Нотатки: {notions_str}, Адреса: {address_str}"

    def add_hashtag_to_notion(self, notion_index, hashtag):
        try:
            notion_index = int(notion_index)
            if 0 <= notion_index < len(self.notions):
                if f"#{hashtag}" not in self.notions[notion_index].hashtags:
                    self.notions[notion_index].hashtags.append(f"#{hashtag}")
                    print(f"Хештег #{hashtag} успішно додано до нотатки.")
                else:
                    print(f"Хештег #{hashtag} вже існує в цій нотатці.")
            else:
                print("Невірний індекс нотатки.")
        except ValueError as e:
            print("Помилка при додаванні хештегу:", e)

    def remove_hashtag_from_notion(self, notion_index, hashtag):
        try:
            notion_index = int(notion_index)
            if 0 <= notion_index < len(self.notions):
                if f"#{hashtag}" in self.notions[notion_index].hashtags:
                    self.notions[notion_index].hashtags.remove(f"#{hashtag}")
                    print(f"Хештег #{hashtag} успішно видалено з нотатки.")
                else:
                    print(f"Хештег #{hashtag} не знайдено в цій нотатці.")
            else:
                print("Невірний індекс нотатки.")
        except ValueError as e:
            print("Помилка при видаленні хештегу:", e)

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, new_address):
        self.address.edit_address(new_address)

    def delete_address(self, address):
        self.address = None
    
    def show_address(self):
        if self.address:
            return self.address.show_address(self.name.value)
        else:
            return "Адреса не знайдена."

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.filename = "contacts_book.json"
        self.load_from_json()

    def add_record(self, record):
        key = record.name.value.lower()
        self.data[key] = record

    def find(self, name):
        name_lower = name.lower()
        return self.data.get(name_lower)

    def delete(self, name):
        name_lower = name.lower()
        if name_lower in self.data:
            del self.data[name_lower]
            return f"Контакт {name} видалено успішно."
        else:
            print("Контакт не знайдено.")

    def find_by_notion_or_hashtag(self, hashtag):
        found_records = []
        for record in self.data.values():
            for notion in record.notions:
                if hashtag in notion.hashtags:
                    found_records.append(record)
                    break  # Зупиняємо пошук, якщо знайдено хештег
        return found_records

    def sort_by_hashtag(self, hashtag):
        sorted_records = []
        for record in self.data.values():
            for notion in record.notions:
                if hashtag in notion.hashtags:
                    sorted_records.append(record.name.value)
                    break  # Зупиняємо, якщо знайдено хештег
        return sorted(sorted_records, key=lambda x: x.lower())

    def all_names(self):
            formatted_names = []
            for name in self.data.keys():
                formatted_name = ' '.join([part.capitalize() for part in name.split()])
                formatted_names.append(formatted_name)
            return formatted_names

    def birthdays(self):
        today = datetime.datetime.now()
        birthdays_this_week = {'Понеділок': [], 'Вівторок': [], 'Середа': [], 'Четвер': [], 'П"ятниця': [], 'Субота': [], 'Неділя': [], 'Сьогодні': []}
        from_day_column_width = 18

        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value
                next_birthday = birthday_date.replace(year=today.year)
                delta_days = (next_birthday - today).days
                birthday_weekday = next_birthday.strftime('%A')

                if next_birthday < today and (birthday_weekday == 'Субота' or birthday_weekday == 'Неділя') and birthday_weekday != 'П"ятниця' and birthday_weekday != 'Четвер':
                    from_day = f' (from {birthday_weekday})'.ljust(from_day_column_width)  # Заповнюємо стовпець from
                    birthdays_this_week['Понеділок'].append((record, from_day)) # Додаємо до списку для понеділка

                # Обробка днів народження для попереднього коду
                if delta_days == 7:
                    if 'Наступний понеділок' not in birthdays_this_week:
                        birthdays_this_week['Наступний понеділок'] = []
                    birthdays_this_week['Наступний понеділок'].append(f"{record.name.value} (will be on {birthday_weekday})")
                elif 0 <= delta_days < 7:
                    if birthday_weekday in ['Субота', 'Неділя']:
                        if 'Наступний понеділок' not in birthdays_this_week:
                            birthdays_this_week['Наступний понеділок'] = []
                        birthdays_this_week['Наступний понеділок'].append(f"{record.name.value} (from {birthday_weekday})")
                    else:
                        birthdays_this_week[birthday_weekday].append(record.name.value)

                # Обробка днів народження для другого коду
                if next_birthday.strftime('%d.%m') == today.strftime('%d.%m'):
                    birthdays_this_week[birthday_weekday].append((record, ''))
                else:
                    if delta_days == 0 and birthday_date.strftime('%d.%m') == today.strftime('%d.%m'):
                        birthdays_this_week['Сьогодні'].append((record, ''))
                    elif 0 <= delta_days < 6:
                        from_day = ''
                        if birthday_weekday == 'Субота' or birthday_weekday == 'Неділя':
                            birthday_weekday = 'Понеділок'
                            from_day = f' (from {birthday_weekday})'.ljust(from_day_column_width)
                        elif record not in birthdays_this_week[birthday_weekday]:
                            birthdays_this_week[birthday_weekday].append((record, from_day))

        print("Майбутні дні народження:")
        upcoming_birthdays = []

        for day, contacts in birthdays_this_week.items():
            if day != 'Сьогодні' and contacts:
                print(f"\n{day}:")
                for contact_data in contacts:
                    if len(contact_data) == 2:
                        contact, from_day = contact_data
                        name_padding = 30 - len(contact.name.value)
                        birthday_padding = 12 - len(contact.show_birthday())
                        from_day_text = from_day if from_day else "".ljust(from_day_column_width)
                        email_padding = 30 - len(contact.show_email())
                        print(
                            Fore.CYAN + f"{contact.name.value}{' ' * name_padding}" +
                            Fore.YELLOW + f"{from_day_text}" +
                            Fore.MAGENTA + " | " +
                            Fore.CYAN + f"{contact.show_birthday()}{' ' * birthday_padding}" +
                            Fore.MAGENTA + " | " +
                            Fore.CYAN + f"{', '.join(str(phone) for phone in contact.phones)}" +
                            Fore.MAGENTA + " | " +
                            Fore.CYAN + f"{contact.show_email()}{' ' * email_padding}" +
                            Fore.MAGENTA + " | " +
                            Style.RESET_ALL
                        )
                    else:
                        # Пропускаємо обробку елемента, який не відповідає очікуваному формату
                        continue

        return upcoming_birthdays
    
    def edit_address(self, name, new_address):
        name_key = name.lower()
        if name_key in self.data:
            record = self.data[name_key]
            if record.address:
                record.address.edit_address(new_address)
                print(f"Адресу для {name} було успішно змінено на {new_address}.")
            else:
                print(f"До {name} ще не додано жодної адреси.")
        else:
            print(f"Контакт {name} не знайдено.")
#_______________________________________________________________________________________________________________________________
    def save_to_json(self, filename="contacts_book.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json_data = []
            for record in self.data.values():
                record_data = {
                    'name': str(record.name),
                    'phones': [str(phone) for phone in record.phones],
                    "email": str(record.email) if record.email else None,
                    'birthday': str(record.birthday) if record.birthday else None,
                    'notions': [{'text': notion.text, 'hashtags': notion.hashtags} for notion in record.notions],
                    "addresses": record.address.addresses if record.address else []
                }
                json_data.append(record_data)
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return "Дані успішно збережено у файлі " + filename + "."

    def load_from_json(self, filename="contacts_book.json"):
        try:
            with open(filename, 'r', encoding= 'utf-8') as f:
                data = json.load(f)
                self.data.clear()
                for record_data in data:
                    record = Record(record_data["name"])
                    for phone in record_data.get("phones", []):
                        record.add_phone(phone)
                    email = record_data.get("email")
                    if email:
                        record.add_email(email)
                    birthday = record_data.get("birthday")
                    if birthday:
                        record.add_birthday(birthday)
                    for notion_data in record_data.get("notions", []):
                        record.add_notion(notion_data["text"], notion_data["hashtags"])
                    addresses = record_data.get("addresses", [])
                    if addresses:
                        for address in addresses:
                            record.add_address(address)
                    self.add_record(record)
            print("Дані успішно завантажено з файлу " + filename + ".")
        except FileNotFoundError:
            print("Файл не знайдено. Буде створено новий файл при збереженні.")
        except json.JSONDecodeError:
            print("Помилка при завантаженні даних. Файл може бути пошкоджений.")
#_______________________________________________________________________________________________________________________________
def command_line_helper(args=None):
    if args is None:
        return print("Щоб побачити меню команд введіть h або help")

    help = ("\nДоступні команди:\n"

            " 1: hello                                                           -- для вітання з ботом\n"
            " 2: h                                                               -- для допомоги\n"
            " 2: help                                                            -- для допомоги\n"
            " 3: add [ім'я] [телефон]                                            -- для додавання контакту\n"
            " 4: change [ім'я] [індекс] [телефон]                                -- для зміни номера контакту\n"
            " 5: phone [ім'я]                                                    -- для отримання номера телефону\n"
            " 6: delete [ім'я]                                                   -- для видалення контакту\n"
            " 7: all                                                             -- для відображення всіх контактів\n"
            " 8: add-email [ім'я] [email]                                        -- для додавання електронної пошти\n"
            " 9: show-email [ім'я]                                               -- для відображення електронної пошти\n"
            " 10: change-email [ім'я] [email]                                    -- для заміни електронної пошти\n"
            " 11: delete-email [ім'я] [email]                                    -- для видалення електронної пошти\n"
            " 12: add-birthday [ім'я] [дата]                                     -- для додавання дня народження\n"
            " 13: show-birthday [ім'я]                                           -- для відображення дня народження\n"
            " 14: birthdays                                                      -- для відображення майбутніх днів народження\n"
            " 15: find-name [ім'я]                                               -- для пошуку за ім'ям\n"
            " 16: find-phone [телефон]                                           -- для пошуку за телефоном\n"
            " 17: find-birth [дата]                                              -- для пошуку за днем народження\n"
            " 18: add-notion [ім'я] [текст] [хештеги]                            -- для додавання нотатки\n"
            " 19: edit-notion [ім'я] [індекс] [новий текст] [нові хештеги]       -- для редагування нотатки\n"
            " 20: delete-notion [ім'я] [індекс]                                  -- для видалення нотатки\n"
            " 21: add-hashtag [ім'я] [індекс нотатки] [хештег]                   -- для додавання хештегу до нотатки\n"
            " 22: remove-hashtag [ім'я] [індекс нотатки] [хештег]                -- для видалення хештегу з нотатки\n"
            " 23: add-address [ім'я]                                             -- для додавання адреси\n"
            " 24: show-address [ім'я]                                            -- для відображення адреси\n"
            " 25: edit-address [ім'я]                                            -- для редагування адреси\n"
            " 26: delete-address [ім'я]                                          -- для видалення адреси\n"
            " 27: save [файл.json]                                               -- для збереження контактів у файл JSON\n"
            " 28: load [файл.json]                                               -- для завантаження контактів з файлу JSON\n"
            "q /good bye/close/exit/quit                                         -- для виходу з програми\n"
            "\n Виберіть цифру 1 до 28 або"  
            "\n Введіть команду повністю:"
            "\n")
    return help
# _______________________________________________________________________________________________________________________________
def command_line_digital_keys(key, command,book):
        email=''

        def command_hello():
            print("Привіт! Як я можу допомогти вам?")

        def command_add():
            name = input("Введіть ім'я контакту: ").strip()
            phone = input("Введіть номер телефону: ").strip()
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"Контакт {name} додано успішно!")

        def command_add_notion():
            if command.startswith("add-notion "):
                parts = command.split(" ", 3)
                if len(parts) >= 4:
                    name, text, hashtags = parts[1], parts[2], parts[3]
                    contact = book.find(name.lower())
                    if contact:
                        contact.add_notion(text, hashtags)
                        print(f"Нотатка додана до контакту {name}.")
                    else:
                        print("Контакт не знайдено.")
                else:
                    print("Недостатньо аргументів. Використовуйте формат: add-notion [ім'я] [текст] [хештеги]")

        def command_find_notions():
            if command.startswith("find-notions "):
                hashtag = command.split(" ", 1)[1]
                results = book.find_by_notion_or_hashtag(hashtag)
                if results:
                    print(f"Знайдені контакти з нотатками, що містять '#{hashtag}':\n")
                    for result in results:
                        for notion in result.notions:
                            if hashtag in notion.hashtags:
                                print(f"{result.name.value}: {notion.text} Хештеги: {' '.join(notion.hashtags)}\n")            
                else:
                    return f"Нотатки з '#{hashtag}' не знайдено."
            
        def command_sort_by_hashtag():
            if command.startswith("sort-by-hashtag "):
                hashtag = command.split(" ", 1)[1]
                sorted_contacts = book.sort_by_hashtag(hashtag)
                if sorted_contacts:
                    print(f"Контакти відсортовані за '#{hashtag}':\n")
                    for contact_name in sorted_contacts:
                        print(contact_name)
                else:
                    print(f"Контакти з '#{hashtag}' не знайдено.")

        def command_change():
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                contact = book.data[name]
                if not contact.phones:
                    phone = input("Введіть номер телефону: ").strip()
                    contact.add_phone(phone)
                else:
                    contact.display_phones()
                    old_phone_index = input("Введіть індекс номеру телефону, який хочете змінити: ")
                    new_phone = input("Введіть новий номер телефону: ").strip()
                    contact.edit_phone(old_phone_index, new_phone)
            else:
                return "Контакт не знайдено!"

        def command_edit_notion():
            if command.startswith("edit-notion "):
                parts = command.split(" ", 4)
                if len(parts) >= 5:
                    name, index, new_text, new_hashtags = parts[1], parts[2], parts[3], parts[4]
                    contact = book.find(name.lower())
                    if contact:
                        contact.edit_notion(int(index), new_text, new_hashtags)
                        print("Нотатку успішно змінено.")
                    else:
                        print("Контакт не знайдено.")
                else:
                    print("Недостатньо аргументів. Використовуйте формат: edit-notion [ім'я] [індекс] [новий текст] [нові хештеги]")

        def command_delete_notion():
            if command.startswith("delete-notion "):
                parts = command.split(" ", 3)
                if len(parts) == 3:
                    name, index = parts[1], parts[2]
                    contact = book.find(name.lower())
                    if contact:
                        contact.delete_notion(int(index))
                        print("Нотатку успішно видалено.")
                    else:
                        print("Контакт не знайдено.")
                else:
                    print("Недостатньо аргументів. Використовуйте формат: delete-notion [ім'я] [індекс]")

        def command_add_hashtag(): 
            if command.startswith("add-hashtag "):
                parts = command.split(" ", 3)
                if len(parts) == 4:
                    name, notion_index, hashtag = parts[1], parts[2], parts[3]
                    contact = book.find(name.lower())
                    if contact:
                        contact.add_hashtag_to_notion(int(notion_index), hashtag)
                        print(f"Хештег #{hashtag} додано до нотатки.")
                    else:
                        print("Контакт не знайдено.")
                else:
                    print("Недостатньо аргументів. Використовуйте формат: add-hashtag [ім'я] [індекс нотатки] [хештег]")

        def command_remove_hashtag():
            if command.startswith("remove-hashtag "):
                parts = command.split(" ", 3)
                if len(parts) == 4:
                    name, notion_index, hashtag = parts[1], parts[2], parts[3]
                    contact = book.find(name.lower())
                    if contact:
                        contact.remove_hashtag_from_notion(
                            int(notion_index), hashtag)
                        print(f"Хештег #{hashtag} видалено з нотатки.")
                    else:
                        print("Контакт не знайдено.")
                else:
                    print("Недостатньо аргументів. Використовуйте формат: remove-hashtag [ім'я] [індекс нотатки] [хештег]")

        def command_phone():
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                print(f"Номер(и) телефону для {book.data[name].name.value}: {', '.join([str(phone) for phone in book.data[name].phones])}")
            else:
                print("Контакт не знайдено!")

        def command_delete():
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                del_contact_name = book.data[name].name.value
                book.delete(name)
                print(f"Контакт {del_contact_name} видалено успішно!")
            else:
                print("Контакт не знайдено!")

        def command_all():
            for record in book.data.values():
                print(record)

        def command_all_names():
            existing_names = book.all_names()
            if existing_names:
                print("Існуючі імена контактів:")
                for name in existing_names:
                    print(name)
            else:
                print("No contacts found.")

        def command_add_birthday():
            name = input("Введіть ім'я контакту: ").strip().lower()
            birthday = input("Введіть день народження (ДД.ММ.РРРР): ").strip()
            if name in book.data:
                book.data[name].add_birthday(birthday)
                print(f"День народження успішно додано для контакту {book.data[name].name.value}!")
            else:
                print("Контакт не знайдено!")

        def command_show_birthday():
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                print(f"День народження для {book.data[name].name.value}: {book.data[name].show_birthday()}")
            else:
                print("Контакт не знайдено!")

        def command_birthdays():
            upcoming_birthdays = book.birthdays()
            print("\nМайбутні дні народження:")
            for name in upcoming_birthdays:
                contact = book.find(name)
                if contact:
                    phone_number = ", ".join(str(phone) for phone in contact.phones) if contact.phones else "Немає номеру телефону"
                    print(f"День народження {name} буде на {contact.birthday}, номер для дзвінка {phone_number}")
                else:
                    print(f"Контакт для {name} не знайдено")

        def command_find_name():
            name_to_find = input("Введіть ім'я для пошуку: ")
            found_contacts = Find.find_by_name(book, name_to_find)
            if found_contacts:
                print("Знайдені контакти:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        def command_find_phone():
            phone_to_find = input("Введіть номер телефону для пошуку: ")
            found_contacts = Find.find_by_phone(book, phone_to_find)
            if found_contacts:
                print("Знайдені контакти:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        def command_find_birth():
            birthday_to_find = input(
                "Введіть день народження для пошуку (ДД.ММ.РРРР): ")
            found_contacts = Find.find_by_birthday(book, birthday_to_find)
            if found_contacts:
                print("Знайдені контакти:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        def command_add_email():
            nonlocal email 
            name = input("Введіть ім'я контакту: ").strip().lower()
            email = input("Введіть адресу електронної пошти: ").strip()
            if name in book.data:
                try:
                    book.data[name].add_email(email)
                except ValueError:
                    print("Неіснуючий формат адреси електронної пошти.\nПовторіть спробу.")
                else:
                    print(f"Додано адресу електронної пошти для контакту {book.data[name].name.value}!")
            else:
                print("Контакт не знайдено!")

        def command_show_email():
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                print(f"Email for {book.data[name].name.value}: {book.data[name].show_email()}")
            else:
                print("Контакт не знайдено!")

        def command_change_email():
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                contact = book.data[name]
                if contact.email:
                    new_email = input("Введіть нову адресу електронної пошти: ").strip()
                    try:
                        contact.edit_email(new_email)
                    except ValueError:
                        print("Неіснуючий формат адреси електронної пошти.\nПовторіть спробу")
                    else:
                        print(f"Змінено адресу електронної пошти для контакту {book.data[name].name.value}!")
                else:
                    print("Контакт не має електронної адреси для редагування.")
            else:
                print("Контакт не знайдено!")

        def command_delete_email():
            nonlocal email
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book:
                record = book[name]
                if record.email is not None:
                    email_to_delete = email
                    record.delete_email(email_to_delete)
                else:
                    print(f"Для {name} не надано електронної пошти.")
            else:
                print(f"Контакт {name} не знайдено!")

        def command_add_address():
            name = input("Введіть назву контакту, до якого ви хочете додати адресу: ")
            name_key = name.lower()
            if name_key in book:
                address = input("Введіть адресу: ").strip()
                record = book[name_key]
                record.add_address(address)
                print(f"Адреса {address} успішно додана до контакту {name}!")
            else:
                print(f"Контакт {name} не знайдено.")

        def command_show_address():
            name = input("Введіть назву контакту, адресу якого ви хочете побачити: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    print(record.address.show_address(record.name.value))
                else:
                    print("Адреса для цього контакту ще не додана або була видалена.")
            else:
                print("Контакт не знайдено.")

        def command_edit_address():
            name = input("Введіть назву контакту, адресу якого ви хочете змінити: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    new_address = input("Введіть нову адресу: ")
                    book.edit_address(name, new_address)
                else:
                    print(f"Адреса ще не додана до контакту {name}.")


        def command_delete_address():
            name = input("Введіть назву контакту, адресу якого ви хочете видалити: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    record.delete_address(record.address.show_address(name))
                    print(f"Адресу контакту {name} успішно видалено.")
                else:
                    print(f"Адреса для цього контакту ще не додана або була видалена.")
            else:
                print(f"Контакт {name} не знайдено.")


        def command_save():
            filename = input(
                "Введіть ім'я файлу для збереження (наприклад, contacts.json): ").strip()
            book.save_to_json(filename)
            print("Контакти успішно збережено!")

        def command_load():
            filename = input(
                "Введіть ім'я файлу для завантаження (наприклад, contacts.json): ").strip()
            book.load_from_json(filename)
            print("Контакти успішно завантажено!")
        
        def command_help():
            help=command_line_helper("help")
            print(help)

        command_dict={
            1: "hello                         -- для допомоги",
            2: "help                          -- для допомоги",
            3: "add [ім'я] [телефон]          -- для додавання контакту",
            4: "change [ім'я] [телефон]       -- для зміни номера контакту",
            5: "phone [ім'я]                  -- для отримання номера телефону",
            6: "delete [ім'я]                 -- для видалення контакту",
            7: "all                           -- для відображення всіх контактів",
            8: "add-email [ім'я] [email]      -- для додавання електронної пошти",
            9: "show-email [ім'я]             -- для відображення електронної пошти",
            10: "change-email [ім'я] [email]  -- для заміни електронної пошти",
            11: "delete-email [ім'я] [email]  -- для видалення електронної пошти",
            12: "add-birthday [ім'я] [дата]   -- для додавання дня народження",
            13: "show-birthday [ім'я]         -- для відображення дня народження",
            14: "birthdays                    -- для відображення майбутніх днів народження",
            15: "find-name [ім'я]             -- для пошуку за іменем",
            16: "find-phone [телефон]         -- для пошуку за телефоном",
            17: "find-birth [дата]            -- для пошуку за днем народження",
            18: "add-notion [ім'я] [текст] [хештеги]                      -- для додавання нотатки",
            19: "edit-notion [ім'я] [індекс] [новий текст] [нові хештеги] -- для редагування нотатки",
            20: "delete-notion [ім'я] [індекс] -- для видалення нотатки",
            21: "add-hashtag [ім'я] [індекс нотатки] [хештег]    -- для додавання хештегу до нотатки", 
            22: "remove-hashtag [ім'я] [індекс нотатки] [хештег] -- для видалення хештегу з нотатки",
            23: "add-address [ім'я]            -- для додавання адреси",
            24: "show-address [ім'я]           -- для відображення адреси",
            25: "edit-address [ім'я]           -- для редагування адреси",
            26: "delete-address [ім'я]         -- для видалення адреси",        
            27: "save [файл.json]              -- для збереження контактів у файл JSON",
            28: "load [файл.json]              -- для завантаження контактів з файлу JSON",
        }

        select_command=command_dict[key]
        print (select_command)
        match (key):
            case 1:
                command_hello()
            
            case 2:
                command_help()
                
            case 3:
                command_add()
            
            case 4:
                command_change()

            case 5:
                command_phone()

            case 6:
                command_delete()

            case 7:
                command_all()

            case 8:
                command_add_email()

            case 9:
                command_show_email()
    
            case 10:
                command_change_email()

            case 11:
                command_delete_email()

            case 12:
                command_add_birthday()

            case 13:
                command_show_birthday()

            case 14:
                command_birthdays()

            case 15:
                command_find_name()

            case 16:
                command_find_phone()

            case 17:
                command_find_birth()

            case 18:
                command_add_notion()

            case 19:
                command_edit_notion()

            case 20:
                command_delete_notion()

            case 21:
                command_add_hashtag()
            
            case 22:
                command_remove_hashtag()
            
            case 23:
                command_add_address()
            
            case 24:
                command_show_address()
            
            case 25:
                command_edit_address()
            
            case 26:
                command_delete_address()

            case 27:
                command_save()
            
            case 28:
                command_load()
#_________________________________________________________________________________________________________________________

def main():
    book = AddressBook()
    print("\nЛаскаво просимо! Вас вітає бот-помічник!")
    command_line_helper()

    while True:
      

        command = input("Введіть команду або цифру від 1 до 28: ")


        if command in ['q', 'good bye', 'close', 'exit', 'quit']:
            break

        elif command in ['h', 'help']:
            help = command_line_helper(command).strip().lower()
            print(help)

        elif command in [str(i) for i in range(1, 21)]:
            command_line_digital_keys(int(command),command,book,)
       
        elif command == 'hello':
            print("\nПривіт! Як я можу допомогти вам?")

        elif command == 'add':
            name = input("\nВведіть ім'я контакту: ").strip()
            name_match = name.lower()
            if name_match in book.data:
                print(f"\nКонтакт з ім'ям '{name}' вже існує. Будь ласка, повторіть команду 'add' та введіть інше ім'я.")
            else:
                while True:
                    phone = input("\nВведіть номер телефону: ").strip()
                    if phone:
                        break
                record = Record(name)
                record.add_phone(phone)
                book.add_record(record)
                print(f"\nКонтакт '{name}' додано успішно!")
                
        elif command == 'add-notion':
            name = input("\nВведіть ім'я контакту до якого ви б хотіли додати нотатку: ")
            name_key = name.lower()
            if name_key in book:
                text = input("\nВведіть текст: ")
                hashtags = get_valid_hashtags() 
                record = book[name_key]
                record.add_notion(text, hashtags)
                print("\nНотатку успішно додано!")
            else:
                print(f"\nКонтакт {name} не знайдено.")

        elif command.startswith("find-notion-by-hashtag"):
            hashtag = input("\nВведіть хештег: ").strip()
            if not hashtag.startswith("#"):
                print("\nДодайте «#» на початку хештегу.")
            else:
                results = book.find_by_notion_or_hashtag(hashtag)
                if results:
                    print(f"\nЗнайдені контакти з нотатками, що містять '{hashtag}':")
                    for result in results:
                        for notion in result.notions:
                            if hashtag in notion.hashtags:
                                print(f"\n{result.name.value}: {notion.text} Хештеги: {' '.join(notion.hashtags)}")
                else:
                    print(f"\nНотатки з '{hashtag}' не знайдено.")

        elif command.startswith("sort-by-hashtag"):
            hashtag = input("\nВведіть хештег: ").strip()
            if not hashtag.startswith("#"):
                print("\nДодайте «#» на початку хештегу.")
            else:
                sorted_contacts = book.sort_by_hashtag(hashtag)
                if sorted_contacts:
                    print(f"\nКонтакти відсортовані за '{hashtag}':")
                    for contact_name in sorted_contacts:
                        print(contact_name)
                else:
                    print(f"\nКонтакти з '{hashtag}' не знайдено.")

        elif command == 'edit-phone':
            name = input("\nВведіть ім'я контакту: ").strip().lower()
            if name in book.data:
                contact = book.data[name]
                if not contact.phones:
                    phone = input("\nВведіть номер телефону: ").strip()
                    contact.add_phone(phone)
                else:
                    contact.display_phones()
                    old_phone_index = input("\nВведіть індекс номеру телефону, який хочете змінити: ")
                    new_phone = input("\nВведіть новий номер телефону: ").strip()
                    contact.edit_phone(old_phone_index, new_phone)
                    print("\nНомер телефону успішно змінено.")
            else:
                print("\nКонтакт не знайдено!")

        elif command.startswith("edit-notion"):
            name = input("\nВведіть ім'я контакту, в якого ви хочете змінити нотатку: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.notions:
                    for i, notion in enumerate(record.notions):
                        print(f"\n{i}: {notion.text} - {' '.join(notion.hashtags)}")
                    index = input("\nВведіть номер нотатки, яку хочете змінити: ")
                    try:
                        index = int(index)
                        if 0 <= index < len(record.notions):
                            new_text = input("\nВведіть новий текст нотатки: ")
                            new_hashtags = input("\nДодайте нові хештеги: ")
                            record.edit_notion(index, new_text, new_hashtags.split())
                            print("\nНотатку успішно змінено!")
                        else:
                            print("\nНеправильний номер нотатки.")
                    except ValueError:
                        print("\nНомер нотатки має бути числом.")
                else:
                    print("\nУ цього контакту немає нотаток.")
            else:
                print(f"\nКонтакт {name} не знайдено.")

        elif command.startswith("delete-notion"):
            name = input("\nВведіть ім'я контакту, в якого ви хочете видалити нотатку: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.notions:
                    for i, notion in enumerate(record.notions):
                        print(f"\n{i}: {notion.text} - {' '.join(notion.hashtags)}")
                    index = input("\nВведіть номер нотатки для видалення: ")
                    try:
                        index = int(index)
                        if 0 <= index < len(record.notions):
                            record.delete_notion(index)
                            print("\nНотатку успішно видалено!")
                        else:
                            print("\nНеправильний номер нотатки.")
                    except ValueError:
                        print("\nНомер нотатки має бути числом.")
                else:
                    print("\nУ цього контакту немає нотаток.")
            else:
                print(f"\nКонтакт {name} не знайдено.")

        elif command == 'add-hashtag':
            name = input("\nВведіть ім'я контакту до якого ви хотіли б додати хештег: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.notions:
                    for i, notion in enumerate(record.notions):
                        print(f"\n{i}: {notion.text} - {' '.join(notion.hashtags)}")
                    index = input("\nВведіть номер нотатки, до якої хочете додати хештег: ")
                    try:
                        index = int(index)
                        if 0 <= index < len(record.notions):
                            new_hashtag = get_valid_hashtags()
                            record.notions[index].hashtags.extend(new_hashtag)
                            print("\nХештег успішно додано!")
                        else:
                            print("\nНеправильний номер нотатки.")
                    except ValueError:
                        print("\nНомер нотатки має бути числом.")
                else:
                    print("\nУ цього контакту немає нотаток.")
            else:
                print(f"\nКонтакт {name} не знайдено.")

        elif command == 'remove-hashtag':
            name = input("\nВведіть ім'я контакту від якого ви хотіли б видалити хештег: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.notions:
                    for i, notion in enumerate(record.notions):
                        print(f"\n{i}: {notion.text} - {' '.join(notion.hashtags)}")
                    index = input("\nВведіть номер нотатки, від якої хочете видалити хештег: ")
                    try:
                        index = int(index)
                        if 0 <= index < len(record.notions):
                            hashtag_to_remove = input("\nВведіть хештег для видалення: ")
                            if hashtag_to_remove in record.notions[index].hashtags:
                                record.notions[index].hashtags.remove(hashtag_to_remove)
                                print("\nХештег успішно видалено!")
                            else:
                                print("\nТакий хештег не знайдено у вибраній нотатці.")
                        else:
                            print("\nНеправильний номер нотатки.")
                    except ValueError:
                        print("\nНомер нотатки має бути числом.")
                else:
                    print("\nУ цього контакту немає нотаток.")
            else:
                print(f"\nКонтакт {name} не знайдено.")

        elif command == 'phone':
            name = input("\nВведіть ім'я контакту: ").strip().lower()
            if name in book.data:
                print(f"\nНомер(и) телефону для {book.data[name].name.value}: {', '.join([str(phone) for phone in book.data[name].phones])}")
            else:
                print("\nКонтакт не знайдено!")

        elif command == 'delete':
            name = input("\nВведіть ім'я контакту: ").strip().lower()
            if name in book.data:
                del_contact_name = book.data[name].name.value
                book.delete(name)
                print(f"\nКонтакт {del_contact_name} видалено успішно!")
            else:
                print("\nКонтакт не знайдено!")

        elif command == 'all':
            for record in book.data.values():
                print(f"\n{record}")
                
        elif command == 'all-names':
            existing_names = book.all_names()
            if existing_names:
                print("\nІснуюючі імена контактів: \n")
                for name in existing_names:
                    print(name)
            else:
                print("\nКонтакти не знайдено.")
        
        elif command == 'add-email':
            name = input("\nВведіть ім'я контакту: ").strip().lower()
            email = input("\nВведіть адресу електронної пошти: ").strip()
            if name in book.data:
                try:
                    book.data[name].add_email(email)
                except ValueError:
                    print("\nНеіснуючий формат адреси електронної пошти.\nПовторіть спробу.")
                else:
                    print(f"\nДодано адресу електронної пошти для контакту {book.data[name].name.value}!")
            else:
                print("\nКонтакт не знайдено!")

        elif command == 'show-email':
            name = input("\nВведіть ім'я контакту: ").strip().lower()
            if name in book.data:
                print(f"\nАдреса електронної пошти {book.data[name].name.value}: {book.data[name].show_email()}")
            else:
                print("\nКонтакт не знайдено!")

        elif command == 'edit-email':
            name = input("\nВведіть ім'я контакту: ").strip().lower()
            if name in book.data:
                contact = book.data[name]
                if contact.email:
                    new_email = input("\nВведіть нову адресу електронної пошти: ").strip()
                    try:
                        contact.edit_email(new_email)
                    except ValueError:
                        print("\nНеіснуючий формат адреси електронної пошти.\nПовторіть спробу")
                    else:
                        print(f"\nЗмінено адресу електронної пошти для контакту {book.data[name].name.value}!")
                else:
                    print("\nКонтакт не має електронної адреси для редагування.")
            else:
                print("\nКонтакт не знайдено!")

        elif command == "delete-email":
            name = input("\nВведіть ім'я контакту: ").strip().lower()
            if name in book:
                record = book[name]
                if record.email is not None:
                    email_to_delete = email
                    record.delete_email(email_to_delete)
                else:
                    print(f"\nДля {name} не надано електронної пошти.")
            else:
                print(f"\nКонтакт {name} не знайдено!")

        elif command == 'add-birthday':
            name = input("\nВведіть ім'я контакту: ").strip().lower()
            birthday = input("\nВведіть день народження (ДД.ММ.РРРР): ").strip()
            if name in book.data:
                book.data[name].add_birthday(birthday)
                print(f"\nДень народження успішно додано для контакту {book.data[name].name.value}!")
            else:
                print("\nКонтакт не знайдено!")

        elif command == 'show-birthday':
            name = input("\nВведіть ім'я контакту: ").strip().lower()
            if name in book.data:
                print(f"\nДень народження для {book.data[name].name.value}: {book.data[name].show_birthday()}")
            else:
                print("\nКонтакт не знайдено!")

        elif command == 'birthdays':
            upcoming_birthdays = book.birthdays()
            print("\nМайбутні дні народження:")
            for name in upcoming_birthdays:
                contact = book.find(name)
                if contact:
                    phone_number = ", ".join(str(phone) for phone in contact.phones) if contact.phones else "Немає номеру телефону"
                    print(f"\nДень народження {name} буде на {contact.birthday}, номер для дзвінка {phone_number}")
                else:
                    print(f"\nКонтакт для {name} не знайдено")

        elif command == 'find-name':
            name_to_find = input("\nВведіть ім'я для пошуку: ")
            found_contacts = Find.find_by_name(book, name_to_find)
            if found_contacts:
                print("\nЗнайдені контакти: ")
                for contact in found_contacts:
                    print(contact)
            else:
                print("\nКонтакти не знайдено.")

        elif command == 'find-phone':
            phone_to_find = input("\nВведіть номер телефону для пошуку: ")
            found_contacts = Find.find_by_phone(book, phone_to_find)
            if found_contacts:
                print("\nЗнайдені контакти: ")
                for contact in found_contacts:
                    print(contact)
            else:
                print("\nКонтакти не знайдено.")

        elif command == 'find-address':
            address_to_find = input("Введіть адресу для пошуку: ")
            found_contacts = Find.find_by_address(book, address_to_find)
            if found_contacts:
                print("Знайдені контакти:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        elif command == 'find-email':
            email_to_find = input("Введіть пошту для пошуку: ")
            found_contacts = Find.find_by_email(book, email_to_find)
            if found_contacts:
                print("Found contacts:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        elif command == 'find-birth':
            birthday_to_find = input("\nВведіть день народження для пошуку (ДД.ММ.РРРР): ")
            found_contacts = Find.find_by_birthday(book, birthday_to_find)
            if found_contacts:
                print("\nЗнайдені контакти: ")
                for contact in found_contacts:
                    print(contact)
            else:
                print("\nКонтакти не знайдено.")

        elif command == 'find-name':
            name_to_find = input("\nВведіть ім'я, яке хочете знайти: ")
            found_contacts = Find.find_by_name(book, name_to_find)
            if found_contacts:
                print("\nЗнайдені контакти: ")
                for contact in found_contacts:
                    print(contact)
            else:
                print("\nКонтакт не знайдено.")

        elif command == 'add-address':
            name = input("\nВведіть ім’я контакту, до якого потрібно додати адресу: ")
            name_key = name.lower()
            if name_key in book:
                while True:
                    address = input("\nВведіть адресу: ").strip()
                    if len(address) > 120:
                        print("\nАдреса перевищує максимально допустиму довжину в 120 символів. Будь ласка спробуйте ще раз.")
                    else:
                        record = book[name_key]
                        record.add_address(address)
                        print(f"\nАдресу {address} успішно додано до контакту {name}!")
                        break
            else:
                print(f"\nКонтакт {name} не знайдено.")

        elif command == "show-address":
            name = input("\nВведіть ім'я контакту, чию адресу ви хочете побачити: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    print(record.address.show_address(record.name.value))
                else:
                    print("\nАдресу цього контакту ще не додано або видалено.")
            else:
                print("\nКонтакт не знайдено.")

        elif command == "edit-address":
            name = input("\nВведіть ім'я контакту, адресу якого ви хочете змінити: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    new_address = input("\nВведіть нову адресу: ")
                    book.edit_address(name, new_address)
                else:
                    print(f"\nДо {name} ще не додано жодної адреси.")

        elif command == "delete-address":
            name = input("\nВведіть ім’я контакту, адресу якого ви хочете видалити: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    record.delete_address(record.address.show_address(name))
                    print(f"\nАдресу для {name} успішно видалено.")
                else:
                    print(f"\nДля {name} не вказано адресу.")
            else:
                print(f"\nКонтакт {name} не знайдено.")

        elif command == 'save':
            while True:
                filename = input("\nВведіть ім'я файлу для збереження (наприклад, contacts.json): ").strip()
                if not filename:
                    print("\nНе введено ім'я файлу. \n Використовується стандартне ім'я 'contacts_book.json'.")
                    filename = "contacts_book.json"
                try:
                    book.save_to_json(filename)
                    print(f"\nКонтакти успішно збережено у файлі {filename}.")
                    break
                except Exception as e:
                    print(f"\nВиникла помилка при збереженні файлу: {e}.")

        elif command == 'load':
            filename = input("\nВведіть ім'я файлу для завантаження (наприклад, contacts.json): ").strip()
            book.load_from_json(filename)
            print("\nКонтакти успішно завантажено!")

        else:
            print("\nНеправильна команда.")

        # Словник доступних команд
        available_commands = {
            "hello": "для вітання з ботом",
            "h": "для допомоги",
            "help": "для допомоги",
            "add": "для додавання контакту",
            "edit-phone": "для зміни номера контакту",
            "phone": "для отримання номера телефону",
            "delete": "для видалення контакту",
            "all": "для відображення всіх контактів",
            "all-names": "для відображення всіх імен",
            "add-email": "для додавання електронної пошти",
            "show-email": "для відображення електронної пошти",
            "edit-email": "для заміни електронної пошти",
            "delete-email": "для видалення електронної пошти",
            "add-birthday": "для додавання дня народження",
            "show-birthday": "для відображення дня народження",
            "birthdays": "для відображення майбутніх днів народження",
            "find-name": "для пошуку за ім'я",
            "find-phone": "для пошуку за телефоном",
            "find-birth": "для пошуку за днем народження",
            "add-notion": "для додавання нотатки",
            "edit-notion": "для редагування нотатки",
            "delete-notion": "для видалення нотатки",
            "add-hashtag": "для додавання хештегу до нотатки",
            "remove-hashtag": "для видалення хештегу з нотатки",
            "find-notion-by-hashtag": "для пошуку нотатки за хештегом",
            "sort-by-hashtag": "для пошуку контактів із зазначеним хештегом",
            "add-address": "для додавання адреси",
            "show-address": "для відображення адреси",
            "edit-address": "для редагування адреси",
            "delete-address": "для видалення адреси",
            "save": "для збереження контактів у файл JSON",
            "load": "для завантаження контактів з файлу JSON",
            "good bye": "для виходу з програми",
            "q": "для виходу з програми",
            "quit": "для виходу з програми",
            "close": "для виходу з програми",
            "exit": "для виходу з програми",

            "1": "для вітання з ботом",
            "2": "для допомоги",
            "2": "для допомоги",
            "3": "для додавання контакту",
            "4": "для зміни номера контакту",
            "5": "для отримання номера телефону",
            "6": "для видалення контакту",
            "7": "для відображення всіх контактів",
            "8": "для додавання електронної пошти",
            "9": "для відображення електронної пошти",
            "10": "для заміни електронної пошти",
            "11": "для видалення електронної пошти",
            "12": "для додавання дня народження",
            "13": "для відображення дня народження",
            "14": "для відображення майбутніх днів народження",
            "15": "для пошуку за ім'я",
            "16": "для пошуку за телефоном",
            "17": "для пошуку за днем народження",
            "18": "для додавання нотатки",
            "19": "для редагування нотатки",
            "20": "для видалення нотатки",
            "21": "для додавання хештегу до нотатки",
            "22": "для видалення хештегу з нотатки",
            "23": "для додавання адреси",
            "24": "для відображення адреси",
            "25": "для редагування адреси",
            "26": "для видалення адреси",
            "27": "для збереження контактів у файл JSON",
            "28": "для завантаження контактів з файлу JSON",
        }

        def suggest_command(user_input):

            matches = [command for command in available_commands.keys() if command.startswith(user_input)]
            if len(matches) == 1:
                return f"Можливо, ви мали на увазі команду: {matches[0]}?\nБудь ласка, спробуйте ще раз."
            elif matches:
                return f"Можливо, ви мали на увазі одну з цих команд: {', '.join(matches)}?\nБудь ласка, спробуйте ще раз."
            else:
                return "Вибачте, я не зрозумів вашу команду. Спробуйте ще раз або введіть 'h' або 'help' для допомоги."


        if command in available_commands:
            pass
        else:
            suggestion = suggest_command(command)
            print(suggestion)


if __name__ == "__main__":
    main()
