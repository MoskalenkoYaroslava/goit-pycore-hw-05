from functools import wraps


def input_error(func):
    """Обробляє помилки введення користувача."""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"

    return inner


def parse_input(user_input):
    """Розділяє введення користувача на команду та аргументи."""
    if not user_input.strip():
        return "", []

    command, *args = user_input.split()
    return command.lower(), args


@input_error
def add_contact(args, contacts):
    """Додає новий контакт."""
    if len(args) < 2:
        raise IndexError

    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    """Змінює номер наявного контакту."""
    if len(args) < 2:
        raise IndexError

    name, phone = args

    if name not in contacts:
        raise KeyError

    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    """Повертає номер телефону контакту."""
    name = args[0]
    return contacts[name]


@input_error
def show_all(contacts):
    """Повертає всі збережені контакти."""
    if not contacts:
        return "No contacts saved."

    return "\n".join(
        f"{name}: {phone}" for name, phone in contacts.items()
    )


def main():
    """Запускає консольного бота."""
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

