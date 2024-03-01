import pickle
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self._value = None
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

class Phone(Field):
    def validate(self, value):
        if not value.isdigit():
            raise ValueError("Phone number contains only digits.")
        
class Email(Field):
    def validate(self, value):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address.")
        
class Tag(Field):
    pass

class Note:
    def __init__(self, text):
        self.text = text
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)

    def __str__(self):
        return f"Note: {self.text}\nTags: {', '.join(tag.text for tag in self.tags)}"

class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y - %M - %d")
        except ValueError:
            raise ValueError('Invalid birthday format. Use "YYYY-MM-DD."')
        
class Contact:
    def __init__(self, first_name, last_name, phone_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = Phone(phone_number)
        self.email = Email(email)

class Record:
    def __init__(self, name, email, phone, favorite = False, birthday = None):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite
        self.birthday = birthday
        self.tags = []
        self.notes = []

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_note(self, note):
        self.notes.append(note)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().data()
            next_birthday = datetime(today.year, self.birthday.month, self.birthday.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.month, self.birthday.day).date()
            return (next_birthday - today).days
        else:
            return None
        
    def __str__(self):
        tags_str = ", ".join(tag.text for tag in self.tags)
        return f"Name: {self.name}\nEmail: {self.email.value}\nPhone: {self.phone.value}\nTags: {tags_str}\n" \
                f"Birthday: {self.birthday.value if self.birthday else 'N/A'}\n"

class AddressBook:
    def __init__(self):
        self.record = []

    def add_record(self, record):
        if isinstance (record, Record):
            self.records.append(record)
        else:
            raise TypeError("Only instances of record can be added to AddresBook.")

    def __iter__(self):
        return iter(self.records)

    def paginate(self, page_size):
        for i in range(0, len(self.records), page_size):
            yield self.records[i:i + page_size]

    def search_contacts(self, query):
        matching_records = []
        for record in self.records:
            if (
                query.lower() in record.name.lover() or
                query.lover() in record.phone.value or
                query.lover() in record.email.value
            ):
                matching_records.append(record)
        return matching_records
    
    def save_to_disk(self, filename = "address_book.pkl"):
        try:
            with open(filename, "wb") as file:
                pickle.dump(self.records, file)
            print("Address book saved successfuly.")
        except Exception as e:
            print(f"Error saving address book: {e}")

    def load_from_disk(self, filename = "address_book.pkl"):
        try:
            with open(filename, "rb") as file:
                self.records = pickle.load(file)
            print("Address book loaded successfully.")
        except FileNotFoundError:
            print("File not found. Creating a new address book.")
        except Exception as e:
            print(f"Error loading address book: {e}")

    def show_all_records(self):
        if not self.records:
            print("Address book is empty.")
        else:
            for record in self.records:
                print(record)

    def create_record():
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        phone_number = input("Enter phone number: ")
        email_address = input("Enter email address: ")

        name = f"{first_name} {last_name}"
        email = Email(email_address)
        phone = Phone(phone_number)

        birthday_input = input("Enter birthday (optional, format YYYY-MM-DD): ")
        try:
            birthday = Birthday(birthday_input) if birthday_input else None
        except ValueError as e:
            print(f"Error: {e}")
            birthday = None

        record = Record(name, email, phone, birthday)

        # Adding Tags
        tags_input = input("Enter tags (comma-separated): ")
        tags = [Tag(tag.strip()) for tag in tags_input.split(",")]
        record.tags.extend(tags)

        #Adding Notes
        notes_input = input("Enter notes (comma-separated): ")
        notes = [Note(note.strip()) for note in notes_input.split(",")]
        record.notes.extend(notes)

        return record
    
    def main(self):
        address_book = AddressBook()
        address_book.load_from_disk()

        while True:
            print("\nChoose an action:")
            print("1. Add a new contact")
            print("2. Search contact")
            print("3. Show all contact")
            print("4. Save address book to disk")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                record = self.create_record()
                address_book.add_record(record)
                print("Contact added successfuly.")
            
            elif choice == "2":
                search_query = input("Enter search query: ")
                matching_records = address_book.search_contacts(search_query)
                if matching_records:
                    print("\nMatching Contacts:")
                    for matching_record in matching_records:
                        print(matching_record)
                else:
                    print("No matching contact found.")

            elif choice == "3":
                address_book.show_all_records()

            elif choice == "4":
                address_book.save_to_disk()

            elif choice == "5":
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    address_book = AddressBook()
    address_book.main()
