from collections import UserDict
from tabulate import tabulate

MOCKED_INPUTS = [
    "hello",
    "record:all",
    "record:add",
    "record:add Mike", # should fail
    "record:add Mike mike", # should fail
    "record:add Mike 01234567891234567", # should fail
    "record:add Mike 01", # should fail
    "record:add Mike 0123456789",
    "record:add Mike 9876543210 0123456789", # should fail
    "record:all",
    "record:find Mike",
    "record:find Mike1234", # should fail
    "record:change Mike", # should fail
    "record:change Mike 01234564567", # should fail
    "record:change Mike 0123456789 9876543210",
    "record:change Mike 0123456789 9876543210", # should fail
    "record:all",
    "phone:add Mike 1111111111",
    "phone:add Mike mmm", # should fail
    "record:all",
    "phone:find Mike",
    "phone:find Mike1234", # should fail
    "record:all",
    "phone:delete Mike 01234564567", # should fail
    "phone:delete Mike 1111111111",
    "record:delete Mike1234", # should fail
    "record:delete Mike",
    "record:all",
]

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit():
            raise ValueError(f"Invalid phone number '{value}'. Phone number must be digits only")
        if len(value) != 10:
            raise ValueError(f"Invalid phone number '{value}'. Phone number must be 10 digits long")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return "Phone number added."

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        raise KeyError(f"Phone number '{value}' not found.")

    def edit_phone(self, old_value, new_value):
        phone = self.find_phone(old_value)
        phone.value = new_value
        return "Phone number changed."

    def delete_phone(self, value):
        phone = self.find_phone(value)
        self.phones.remove(phone)
        return "Phone number deleted."

    def __str__(self):
        phone_list = '; '.join(p.value for p in self.phones) if self.phones else 'No phones'
        return f"Contact name: {self.name.value}, phones: {phone_list}"

class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            raise KeyError(f"Contact '{record.name.value}' already exists.")
        self.data[record.name.value] = record
        return "Contact added."

    def find(self, name):
        if not name in self.data:
            raise KeyError(f"Contact '{name}' not found.")
        return self.data[name]

    def delete(self, name):
        if not name in self.data:
            raise KeyError(f"Contact '{name}' not found.")
        del self.data[name]
        return "Contact deleted."

    def __str__(self):
        table = []
        for name, record in self.data.items():
            table.append([name, '; '.join(p.value for p in record.phones)])
        return tabulate(table, headers=['Name', 'Phone'], tablefmt='orgtbl')

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def format_error_msg(msg):
    return "\033[91m" + msg + "\033[0m"

def format_success_msg(msg):
    return "\033[92m" + msg + "\033[0m"

def format_warning_msg(msg):
    return "\033[93m" + msg + "\033[0m"

class CommandHandler:
    def __init__(self, book):
        self.book = book
        self.init_test_records()

    def init_test_records(self):
        test_records = {
            "John": ["1234567890", "5555555555"],
            "Jane": ["9876543210"],
            "Kate": ["1231231231"],
            "Alex": ["3213213213"],
        }
        for name, phones in test_records.items():
            record = Record(name)
            for phone in phones:
                record.add_phone(phone)
            self.book.add_record(record)

    def handle_add(self, args):
        if len(args) < 2:
            raise ValueError("Name and phone must be specified")
        new_record = Record(args[0])
        new_record.add_phone(args[1])
        return self.book.add_record(new_record)

    def handle_find(self, name):
        return self.book.find(name)

    def handle_change(self, args):
        if len(args) < 3:
            raise ValueError("Name, old and new phone must be specified")
        record = self.book.find(args[0])
        return record.edit_phone(args[1], args[2])

    def handle_delete_record(self, name):
        return self.book.delete(name)

    def handle_add_phone(self, args):
        if len(args) < 2:
            raise ValueError("Name and phone must be specified")
        record = self.book.find(args[0])
        return record.add_phone(args[1])

    def handle_delete_phone(self, args):
        if len(args) < 2:
            raise ValueError("Name and phone must be specified")
        record = self.book.find(args[0])
        return record.delete_phone(args[1])
    
    def autotest(self):
        for input_cmd in MOCKED_INPUTS:
            print(f"\nExecuting command: {format_warning_msg(input_cmd)}")
            command, *args = parse_input(input_cmd)
            self.execute_command(command, args)

    def execute_command(self, command, args):
        try:
            if command == "autotest":
                self.autotest()
                return
            if command == "record:add":
                print(format_success_msg(self.handle_add(args)))
            elif command == "record:find":
                print(self.handle_find(args[0]))
            elif command == "record:change":
                print(format_success_msg(self.handle_change(args)))
            elif command == "record:delete":
                print(format_success_msg(self.handle_delete_record(args[0])))
            elif command == "record:all":
                print(self.book)
            elif command == "phone:find":
                record = self.book.find(args[0])
                print(record)
            elif command == "phone:add":
                print(format_success_msg(self.handle_add_phone(args)))
            elif command == "phone:delete":
                print(format_success_msg(self.handle_delete_phone(args)))
            elif command == "hello":
                print("How can I help you?")
            elif command == "help":
                print("Available Commands:")
                print("  - autotest: Run the autotest")
                print("  - hello: Greet the bot")
                print("  - record:add <name> <phone>: Add a new contact")
                print("  - record:find <name>: Find a contact")
                print("  - record:change <name> <old_phone> <new_phone>: Change an existing contact")
                print("  - record:delete <name>: Delete an existing contact")
                print("  - record:all: Get all contacts")
                print("  - phone:add <name> <phone>: Add a new phone to a contact")
                print("  - phone:find <name>: Get the phone number of a contact")
                print("  - phone:delete <name> <phone>: Delete a phone from a contact")
                print("  - help: Print this message")
                print("  - exit, close, bye: Exit the assistant bot")
            else:
                print(format_error_msg("Invalid command."))
        except (KeyError, ValueError) as e:
            print(format_error_msg(str(e)))

def main():
    book = AddressBook()
    handler = CommandHandler(book)

    print("Welcome to the assistant bot written with classes!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "bye"]:
            print("Good bye!")
            break

        handler.execute_command(command, args)


if __name__ == "__main__":
    main()