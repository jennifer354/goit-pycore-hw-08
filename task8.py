from datetime import datetime
import pickle
class Birthday:
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_birthday(self, value):
        self.birthday = Birthday(value)

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find(self, name):
        for record in self.records:
            if record.name == name:
                return record
        return None

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.records:
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                if 0 <= (birthday_this_year - today).days <= 7:
                    if birthday_this_year.weekday() >= 5:
                        birthday_this_year = self.find_next_weekday(birthday_this_year, 0)
                    upcoming_birthdays.append({
                        "name": record.name,
                        "congratulation_date": birthday_this_year.strftime('%d.%m.%Y')
                    })
        return upcoming_birthdays

    @staticmethod
    def find_next_weekday(d, weekday: int):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + timedelta(days=days_ahead)

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return str(e)
        except IndexError:
            return "Invalid command format."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Provide both name and phone number.")
    
    name, phone = args
    if not phone.startswith("+380") or not phone[4:].isdigit() or len(phone) != 13:
        raise ValueError("Phone number should be in the format +380XXXXXXXXX.")
    
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.phones.append(phone)
    return message

@input_error
def change_contact(args, book):
    if len(args) != 2:
        raise ValueError("Provide both name and phone number.")
    
    name, phone = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    
    if not phone.startswith("+380") or not phone[4:].isdigit() or len(phone) != 13:
        raise ValueError("Phone number should be in the format +380XXXXXXXXX.")
    
    record.phones = [phone]
    return "Contact updated successfully"

@input_error
def show_contact(args, book):
    if len(args) != 1:
        raise ValueError("Provide a name to show the contact.")
    name = args[0]
    record = book.find(name)
    if record:
        phones = ', '.join(record.phones) if record.phones else "No phone number set."
        return f"Name: {record.name}, Phone: {phones}"
    else:
        return f"Contact '{name}' not found."

@input_error
def show_all_contacts(book):
    if book.records:
        for record in book.records:
            phones = ', '.join(record.phones) if record.phones else "No phone number set."
            print(f"Name: {record.name}, Phone: {phones}")
    else:
        return "Address book is empty."

@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Provide both name and birthday in the format DD.MM.YYYY.")
    
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Provide a name to show the birthday.")
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record:
        return f"{name} does not have a birthday set."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_upcoming_birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{birthday['name']}'s birthday: {birthday['congratulation_date']}" for birthday in upcoming_birthdays])
    else:
        return "No upcoming birthdays."

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  


def main():
    
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
        
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        
        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_contact(args, book))

        elif command == "all":
            show_all_contacts(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_upcoming_birthdays(book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
