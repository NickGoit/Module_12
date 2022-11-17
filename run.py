from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __str__(self):
        return f'{self.value}'


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        # if new_value.startswith('+38'):
        #     self.__value = new_value
        # else:
        #     print('Wrong number type')
        for elem in new_value:
            if elem in ('+', '-', '(', ')', ' '):
                new_value = new_value.replace(elem, '')
        if new_value.isdecimal():
            self.__value = f'+{new_value}'
        else:
            print('Please type a phone in format "+***-***-***-*"')

    def __repr__(self):
        return f'{self.value}'

    def __eq__(self, o):
        return self.value == o.value


class Birthday:
    def __init__(self):
        self._birthday = datetime

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, birthday_str):
        birth_list = birthday_str.split('.')
        if (len(birth_list) < 3) or (len(birth_list) > 3):
            print('Please type birthday in format "year.month.day"')
        year = [num for num in birth_list if len(num) == 4]
        year_index_in_list = birth_list.index(year[0])
        index_day = [2 if year_index_in_list == 0 else 0]
        year = int(year[0])
        month = int(birth_list[1])
        day = int((birth_list[index_day[0]]))
        self._birthday = datetime(year=year, month=month, day=day).date()

    def __str__(self):
        return f'{self._birthday}'

    def day_to_next_birthday(self):
        current_year = datetime.now().year
        current_day = datetime.now()
        this_year_birthday = datetime(year=current_year, month=self._birthday.month, day=self._birthday.day)
        if (this_year_birthday - current_day).days >= 0:
            next_birth = this_year_birthday-current_day
            return f'Days to birthday is {next_birth.days}'
        else:
            next_birth = datetime(year=current_year+1, month=self._birthday.month, day=self._birthday.day)
            return f'Days to birthday is {(next_birth-current_day).days}'


class Record:

    def __init__(self, name_in, phone=None, birth_str=None):
        self.name = Name(name_in)
        self.phones = [Phone(phone) if phone else []]
        self.birth = birth_str

    def __repr__(self):
        return f'{self.name} {self.phones} {self.birth}'

    def __str__(self):
        return f'name:{self.name} phone:{self.phones} {self.birth}'

    def adding_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones.remove(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.adding_phone(new_phone)

    def edit_name(self, new_name):
        self.name = Name(new_name)

    def days_to_birthday(self):
        birth = Birthday()
        birth.birthday = self.birth
        return birth.day_to_next_birthday()


class AdressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        self.number_data = 0

    def edit_record(self, name, old_phone, new_phone):
        local_record = self.data[name]
        local_record.edit_phone(old_phone, new_phone)

    def remove_record(self, record):
        self.data.pop(record.name.value)

    def find_record(self, name):
        error_text = f'Contact {name} is not found at AdressBook'
        return self.data[name] if name in self.data else error_text

    def show_all_book(self):
        return list(self.data.values())

    def __iter__(self):
        i = 0
        list_data = []
        for value in self.data.values():
            list_data.append(value)
        while i <= len(self.data):
            result = list_data[i:i+2]
            yield result
            i += 2

    def __str__(self):
        return f'{list(self.data.values())}'

    # def __repr__(self):
    #     return f'{self.data.values()}'


address_book = AdressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact is not found. Please try again'
        except ValueError:
            return 'Please enter your data correctly and try again'
        except IndexError:
            return 'Please check arguments'
        except TypeError:
            return 'Please enter correct data with space'
    return wrapper


@input_error
def greetings_fun():
    return 'Greeting, How can I help you?'


@input_error
def adding_fun(name, phone, birthday=None):
    # CONTACTS[name] = phone              # Було так
    record = Record(name, phone, birthday)        # Має стати так
    address_book.add_record(record)
    return f'Contact {name} and phone(s) {phone} was successfully added'


@input_error
def change_fun(name, old_phone, new_phone):
    # CONTACTS[name] = new_phone
    address_book.edit_record(name, old_phone, new_phone)
    return f'Contact {name} has changed phone number on {new_phone}'


@input_error
def find_fun(name):
    return f'Under the {name} contact is recorded phone {address_book.find_record(name)}'


@input_error
def show_all_fun():
    database = ''
    if address_book:
        for data in address_book:
            database += f'{data}\n'
        return database
    else:
        return 'Contacts database is empty'


@input_error
def goodbay_fun():
    return 'Thank you for applying our Bot-assist. Have a nice day'


def reaction(user_command, *data):
    if user_command in COMMANDS:
        return COMMANDS[user_command](*data)
    else:
        return 'Wrong command'


def data_analytic(data):
    if data == 'show all':
        user_command = 'show all'
        arguments = tuple()
        return reaction(user_command, *arguments)

    if data == 'good bye':
        user_command = 'good bye'
        arguments = tuple()
        return reaction(user_command, *arguments)

    (user_command, *arguments) = data.casefold().split()
    return reaction(user_command, *arguments)


COMMANDS = {
    'hello': greetings_fun,
    'add': adding_fun,
    'change': change_fun,
    'phone': find_fun,
    'show all': show_all_fun,
    'good bye': goodbay_fun,
    'close': goodbay_fun,
    'exit': goodbay_fun
}


def main():
    while True:
        request = input('Please type command: ')
        result = data_analytic(request)
        print(result)
        if result == 'Thank you for applying our Bot-assist. Have a nice day':
            break


if __name__ == '__main__':
    main()
    # birth1 = Birthday()
    # print(birth1)
    # birth1.birthday = '14.11.1988'
    # print(birth1)
    # print(birth1.day_to_next_birthday())
    # record1 = Record('Nick','+38245', '1985.11.18')
    # ab = AdressBook()
    # ab.add_record(record1)
    # print(ab.show_all_book())
    #print(record1)
    # print(record1)
    # print(record1.days_to_birthday())
    # phone1 = Phone('+385-5754-5454-5')
    # print(phone1.value)




