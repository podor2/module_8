import pickle
from objects import *
import traceback



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "No command or wrong arguments given. Please try again"
        except IndexError:
            return "Arguments for command missing. Please try again"
        except KeyError:
            return "Contact not found"
        except AttributeError:
            return "Contact not found"
        except CustomError as e:
            return e.message
        except Exception as e:
            return f"{traceback.format_exc()} \nDear User, Sorry for this error :( . You can report this error to 'goit_support_team@gmail.com' and we will fix it."
    return inner


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

@input_error
def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(contacts: AddressBook, args):
    phone = None
    if len(args) > 1:
        name, phone, *_ = args
    else:
        name = args[0]
    message = "Contact updated"
    record = contacts.find(name)
    if not record:
        record = Record(name)
        contacts.add_record(record)
        message = "Contact added"
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_phone(contacts: AddressBook, args):
    name, old_phone, new_phone, *_ = args
    record = contacts.find(name)
    if not record:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return 'Contact changed'


@input_error
def show_phones(contacts, args):
    name, *_ = args
    record = contacts.find(name)
    if not record:
        raise KeyError
    elif record.phones:
        return [phone.value for phone in record.phones]
    else:
        return f"No phone numbers of {name} recorded "


@input_error
def find_phone(contacts, args):
    phone, *_ = args
    for record in contacts.values():
        match = record.find_phone(phone)
        if match:
            return f'{phone} is phone number of {record.name}'
    raise CustomError('phone not found')


@input_error
def remove_phone(contacts, args):  # add error
    name, phone, *_ = args
    record = contacts.find(name)
    if not record:
        raise KeyError
    else:
        record.remove_phone(phone)
        return f"phone deleted"


@input_error
def delete_contact(contacts, args):
    name, *_ = args
    contacts.delete(name)
    return f"{name.capitalize()} contact deleted"


@input_error
def add_birthday(contacts, args):
    name, birthday, *_ = args
    record = contacts.find(name)
    if not record:
        raise KeyError
    else:
        record.add_birthday(birthday)
        return "Birthday added"


@input_error
def show_birthday(contacts, args):
    name, *_ = args
    record = contacts.find(name)
    if not record:
        raise KeyError
    elif not record.birthday:
        return f"Birtday of {name} is not assigned"
    else:
        return f"Birhtday of {record.name} is {record.birthday}"


@input_error
def all_birthdays(contacts, args):
    upcoming_birthdays = contacts.get_upcoming_birtdays()
    if upcoming_birthdays:
        return upcoming_birthdays
    return "No birthays in next 7 days"


def all_commands(contacts, *_):
    return contacts


def help_command(*_):
    return '''List of available commands :
"add (name) (phone)" : add person to the contact book. phone number will be also added if given;
"change (name) (old phone) (new phone)" : changes old phone of stated perosn to new phone;
"phone (phone)" : find the phone across all contacts and return contact and phone;
"remove (name) (phone)" : removes given phone number from phone number list of given contact;
"phones (name)" : returns all phone numbers of given contact;
"delete (name)" : deletes record of given contact;
"all" : returns all saved contacts and phones;
"add-birthday (name) (phone)" : add birth date to given contact;
"show-birthday (name)" : returns birth date of given contact;
"birthdays" : returns list of persons and congratulation date of the next 7 days;
"help" : returns the list of all availible commands;
"close" or "exit" : finishes programm execution'''


def main():
    contacts = load_data()
    commands = {'add': add_contact, 'change': change_phone, 'phone': find_phone, 'remove': remove_phone, 'phones': show_phones, 'delete': delete_contact, 'all': all_commands, 'add-birthday': add_birthday,
                'show-birthday': show_birthday, 'birthdays': all_birthdays, 'help': help_command}

    print('Good Day, User, How can i help you ? To see a list of comands use command "help".\n')
    while True:
        user_input = input("Please write command\n")
        command, *args = parse_input(user_input)
        if command in ['close', 'exit']:
            save_data(contacts)
            print('Goodbye, User!')
            break
        elif command == "hello":
            print("Hello, User! How can I help you ?")
        elif command in commands:
            print(commands[command](contacts, args))
        else:
            print("Command is not identified")


if __name__ == '__main__':
    main()
