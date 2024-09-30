from collections import UserDict
from datetime import datetime, date, timedelta
import re


class CustomError(Exception) :
    def __init__(self, message) :
        self.message = message
        super().__init__(self.message)


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):

    def __init__(self, value):
        value = value.capitalize()
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if re.fullmatch(r'\d{10}', value):
            super().__init__(value)
        else:
            raise CustomError("phone number should be 10 figures long")
        


class Birthday(Field):
    def __init__(self, value):
        try:
            self.string_to_date(value)
        except ValueError:
            raise CustomError("Invalid date format. Use DD.MM.YYYY")
        else : 
            super().__init__(value)

    def string_to_date(self, date_string):
        return datetime.strptime(date_string, "%d.%m.%Y").date()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        founded_phone = self.find_phone(phone)
        if founded_phone:
            self.phones.remove(founded_phone)
        else:
            raise CustomError("This number not found")

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for phone_object in self.phones:
            if phone_object.value == phone:
                return phone_object
        else :
            return None

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        name = name.capitalize()
        if name in self.data.keys():
            return self.data[name]
        else :
            return None
        

    def delete(self, name):
        try :
            del self.data[name.capitalize()]
        except KeyError :
            raise CustomError('Contact not found')

    def date_to_string(self, date):
        return date.strftime("%d.%m.%Y")
    
    def string_to_date(self, date_string):
        return datetime.strptime(date_string, "%d.%m.%Y").date()

    def give_birthdays(self):
        prepared_list = []
        for person in self.data.values():
            if person.birthday:
                prepared_list.append(
                    {"name": person.name.value, "birthday": self.person.birthday.value})
        return prepared_list

    def get_upcoming_birtdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        def find_next_weekday(start_date, weekday):
            days_ahead = weekday - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return start_date + timedelta(days=days_ahead)

        def adjust_for_weekend(birthday):
            if birthday.weekday() >= 5:
                return find_next_weekday(birthday, 0)
            return birthday

        for person in self.data.values():
            
            if person.birthday :
                persons_birthday = self.string_to_date(person.birthday.value)
                birthday_this_year = persons_birthday.replace(year=today.year)
                
                if birthday_this_year < today:

                    birthday_this_year = birthday_this_year.replace(year=2025)

                if 0 <= (birthday_this_year - today).days <= days:
                    birthday_this_year = adjust_for_weekend(birthday_this_year)

                    congratulation_date_str = self.date_to_string(
                        birthday_this_year)
                    upcoming_birthdays.append(
                        {"name": person.name.value, "congratulation_date": congratulation_date_str})
            else :
                pass 
        return upcoming_birthdays

    def __str__(self):
        return f"List of availible contacts:\n{'\n'.join(f'\t{str(record)}' for record in self.data.values())}"

