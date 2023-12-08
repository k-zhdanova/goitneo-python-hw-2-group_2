from tabulate import tabulate

def input_error(func):
    def inner(args, contacts):
        command = func.__name__
        try:
            validate_args(args, command)
            return func(args, contacts)
        except ValueError as e:
            return format_error_msg(str(e))
        except KeyError:
            return format_error_msg("Contact not found.")
        except IndexError:
            return format_error_msg("Invalid command format.")
    return inner

def validate_args(args, command):
    if command in ["add_contact", "change_contact"]:
        if len(args) != 2:
            raise ValueError("Invalid number of arguments. Please provide name and phone.")
        if not args[1].isdigit():
            raise ValueError("Invalid phone number. Please enter digits only.")
    elif command in ["remove_contact", "get_phone"]:
        if len(args) != 1:
            raise ValueError("Invalid number of arguments. Please provide only the name.")

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact changed."
    else:
        return format_error_msg("Contact not found.")

@input_error
def remove_contact(args, contacts):
    name, = args
    if name in contacts:
        del contacts[name]
        return "Contact removed."
    else:
        return format_error_msg("Contact not found.")

@input_error
def get_phone(args, contacts):
    name, = args
    if name in contacts:
        return contacts[name]
    else:
        return format_error_msg("Contact not found.")

def get_all_contacts(contacts):
    contacts_data = []
    for contact in contacts:
        contacts_data.append([contact, contacts[contact]])

    head = ["Name", "Phone"]
    return tabulate(contacts_data, headers=head, tablefmt="grid")

def format_error_msg(msg):
    return "\033[91m" + msg + "\033[0m"

def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input = input("Enter a command: ")

            try: 
                command, *args = parse_input(user_input)
            except ValueError:
                print(format_error_msg("Invalid command."))
                continue

            if command in ["close", "exit", "bye"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                result = add_contact(args, contacts)
                print(result)
            elif command == "change":
                result = change_contact(args, contacts)
                print(result)
            elif command == "remove":
                result = remove_contact(args, contacts)
                print(result)
            elif command == "phone":
                result = get_phone(args, contacts)
                print(result)
            elif command == "all":
                result = get_all_contacts(contacts)
                print(result)
            elif command == "help":
                print("Available Commands:")
                print("  - hello: Greet the bot")
                print("  - add <name> <phone>: Add a new contact")
                print("  - change <name> <phone>: Change an existing contact")
                print("  - remove <name>: Remove an existing contact")
                print("  - phone <name>: Get the phone number of a contact")
                print("  - all: Get all contacts")
                print("  - help: Print this message")
                print("  - exit, close, bye: Exit the assistant bot")
            else:
                print(format_error_msg("Invalid command."))
        except KeyboardInterrupt:
            print("\nGood bye!")
            break
        except ValueError as e:
            print(format_error_msg(str(e)))
            continue

if __name__ == "__main__":
    main()