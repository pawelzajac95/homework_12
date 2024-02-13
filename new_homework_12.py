from collections import UserDict
from datetime import datetime
import pickle


def save_address_book(address_book, filename):
    with open(filename, 'wb') as fh:
        pickle.dump(address_book, fh)


def load_address_book(filename):
    with open(filename, 'rb') as fh:
        address_book = pickle.load(fh)
    return address_book


class Field:
    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):

        if new_value is not None and len(str(new_value)) == 9 and str(new_value).isdigit():
            self._value = new_value
        else:
            raise ValueError(
                "Invalid phone number. Please provide a valid 9-digit number.")


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):

        if new_value is None or isinstance(new_value, datetime):
            self._value = new_value
        else:
            raise ValueError(
                "Invalid birthday date. Please provide a valid datetime object or None.")


class Record:

    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.now()
            next_birthday = self.birthday.value.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_until_birthday = (next_birthday - today).days
            return days_until_birthday
        else:
            return None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, address_book):
        name = self.name.value
        if name in address_book.data:
            del address_book.data[name]
        else:
            raise KeyError

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def search_contacts(self, address_book, query):
        found_contacts = []
        for records in address_book.data.values():
            if query.isdigit():
                for phone in records.phones:
                    if query in phone.value:
                        found_contacts.append(records)
                        break
            elif query.lower() in records.name.value.lower():
                found_contacts.append(records)
        return found_contacts


class AddressBook(UserDict):
    def add_record(self, record):
        key = record.name.value
        self.data[key] = record

    def find_record(self, name):
        record = self.data.get(name)
        if record:
            return record
        else:
            return None

    def __iter__(self):
        self.records = list(self.data.values())
        self.current_index = 0
        self.page_size = 100
        return self

    def __next__(self):
        keys = list(self.data.keys())
        if self.current_index >= len(keys):
            raise StopIteration
        keys_slice = keys[self.current_index:self.current_index + self.page_size]
        self.current_index += self.page_size
        return [self.data[key] for key in keys_slice]


def main():
    address_book = AddressBook()

    while True:
        try:
            command = input("Enter command: ")
    
            if command == "hello":
                print("How can I help you?")
    
            elif command.startswith("add"):
                _, first_name, last_name, phone_number, * \
                    birthday_input = command.split(" ", 4)
                name = f'{first_name} {last_name}'
                record = Record(name)
                record.add_phone(phone_number)
                if birthday_input:
                    try:
                        birthday_date = datetime.strptime(
                            birthday_input[0], "%Y-%m-%d")
                        record.birthday = Birthday(birthday_date)
                    except ValueError:
                        print(
                            "Invalid birthday date format. Please enter date in YYYY-MM-DD format.")
                address_book.add_record(record)
                print("Contact added successfully.")
    
            elif command.startswith("change"):
                _, first_name, last_name, new_phone_number = command.split(
                    " ", 3)
                name = f'{first_name} {last_name}'
                record = address_book.find_record(name)
                if record:
                    record.edit_phone(record.phones[0].value, new_phone_number)
                    print("Phone number updated successfully.")
                else:
                    print("Contact not found.")
    
            elif command.startswith("find"):
                _, first_name, last_name = command.split(" ", 2)
                name = f'{first_name} {last_name}'
                found_records = address_book.find_record(name)
                if found_records:
                    for phone in found_records.phones:
                        print(f'{found_records.name.value} Phone: {
                            phone.value}')
                    if found_records.birthday.value:
                        print(f'{found_records.name.value} Birthday: {
                            found_records.birthday.value.date()}')
                        days_until_birthday = found_records.days_to_birthday()
                        print(f"Days until next birthday: {
                            days_until_birthday}")
                else:
                    raise ValueError('Contact not found')
    
            elif command.startswith("delete"):
                _, first_name, last_name = command.split(" ", 2)
                name = f'{first_name} {last_name}'
                record = address_book.find_record(name)
                if record:
                    record.remove_phone(address_book)
                    print('Contact deleted successfully')
                else:
                    print("Contact not found.")
    
            elif command.startswith("list"):
                for page in (address_book):
    
                    for record in page:
                        print(f"Name: {record.name.value}")
                        for phone in record.phones:
                            print(f"Phone: {phone.value}")
                        if record.birthday.value:
                            print(f"Birthday: {record.birthday.value.date()}")
                            days_until_birthday = record.days_to_birthday()
                            print(f"Days until next birthday: {
                                days_until_birthday}")
                        print()
    
            elif command.startswith("search"):
                _, query = command.split(" ", 1)
    
                found_contacts = record.search_contacts(
                    address_book, query)
                if found_contacts:
                    print("Found contacts:")
                    for contact in found_contacts:
                        print(f"Name: {contact.name.value}")
                        for phone in contact.phones:
                            print(f"Phone: {phone.value}")
                        if contact.birthday.value:
                            print(f"Birthday: {contact.birthday.value.date()}")
                            days_until_birthday = contact.days_to_birthday()
                            print(f"Days until next birthday: {
                                  days_until_birthday}")
                        print()
                else:
                    print("No contacts found.")
    
            elif command == 'save':
                save_address_book(address_book, "address_book.txt")
                print('Address book saved successfully.')
    
            elif command == 'load':
                try:
                    address_book = load_address_book('address_book.txt')
                    print('Address book loaded successfully.')
                except FileNotFoundError:
                    print('No existing address book found')
    
            elif command in ["goodbye", "close", "exit", "."]:
                print("Goodbye!")
                break
    
            else:
                print("Invalid command. Please try again.")

        except Exception as e:
            print(f'Error: {e}')


if __name__ == "__main__":
    main()
