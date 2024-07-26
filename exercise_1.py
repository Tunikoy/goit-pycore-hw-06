from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return
        raise ValueError("Old phone number not found.")

    def find_phone(self, phone_number):
        for p in self.phones:
            if p.value == phone_number:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the argument for the command."
    return inner

def main():
    address_book = AddressBook()

    while True:
        command_input = input("Enter a command: ").strip().lower()
        
        if command_input in ['exit', 'close']:
            print("Exiting program...")
            break
        elif command_input == 'hello':
            print("How can I help you?")
        else:
            command, args = parse_input(command_input)

            if command == 'add':
                if len(args) == 2:
                    name, phone_number = args
                    record = address_book.find(name)
                    if not record:
                        record = Record(name)
                        address_book.add_record(record)
                    record.add_phone(phone_number)
                    print(f"Contact '{name}' added with phone number {phone_number}.")
                else:
                    print("Give me name and phone please.")
            elif command == 'change':
                if len(args) == 3:
                    name, old_phone, new_phone = args
                    record = address_book.find(name)
                    if record:
                        try:
                            record.edit_phone(old_phone, new_phone)
                            print(f"Phone number for '{name}' updated from {old_phone} to {new_phone}.")
                        except ValueError as e:
                            print(e)
                    else:
                        print("Contact not found.")
                else:
                    print("Give me name, old phone, and new phone please.")
            elif command == 'phone':
                if len(args) == 1:
                    name = args[0]
                    record = address_book.find(name)
                    if record:
                        print(f"Phone numbers for '{name}': {'; '.join(p.value for p in record.phones)}")
                    else:
                        print("Contact not found.")
                else:
                    print("Give me name please.")
            elif command == 'all':
                if address_book.data:
                    for name, record in address_book.data.items():
                        print(record)
                else:
                    print("No contacts found.")
            elif command == 'delete':
                if len(args) == 1:
                    name = args[0]
                    address_book.delete(name)
                    print(f"Contact '{name}' deleted.")
                else:
                    print("Give me name please.")
            else:
                print("Invalid command. Please try again.")

@input_error
def parse_input(command_input):
    parts = command_input.split()
    if len(parts) == 0:
        raise IndexError
    command = parts[0]
    args = parts[1:]
    return command, args

if __name__ == "__main__":
    print("Welcome to the assistant bot!")
    main()
