import database_logic as db
import validators as input_defense

# ANSI escape codes for clear user feedback


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'


# Sets up the DB
db.init_db()

# Menu loop
while True:
    menu = input(f'''{Colors.CYAN}{Colors.BOLD}
                1. Enter book
                2. Update book
                3. Delete book
                4. Search books
                5. View details of all books
                0. Exit
                {Colors.END}Selection: ''')

    # Control flow for adding a new book
    if menu == "1":
        # 1. Author logic
        while True:
            # Gathers user input and validates it
            raw_author_id = input("Author ID: ")
            clean_author_id = input_defense.validate_four_digit_id(
                raw_author_id)
            # Checks if that author already exists
            if clean_author_id:
                if not db.author_exists(clean_author_id):
                    print(
                        f"{Colors.YELLOW}Author ID {clean_author_id} not found"
                        f". Please provide details:{Colors.END}")
                    # Gathers user input if it's a new author
                    author_name = input("Author Name: ")
                    author_country = input("Author Country: ")
                    # Adds new author to db
                    db.add_author(clean_author_id, author_name, author_country)
                    print(
                        f"{Colors.GREEN}New author added successfully."
                        f"{Colors.END}")
                    break
                else:
                    break

        # 2. Book ID Logic
        while True:
            # Gathers user input and validates it
            raw_id = input("Book ID: ")
            clean_id = input_defense.validate_four_digit_id(raw_id)
            # Checks if that book already exists
            if clean_id:
                if db.book_exists(clean_id):
                    print(
                        f"{Colors.RED}Error: Book ID {clean_id} "
                        f"already exists!{Colors.END}")
                else:
                    break

        title = input("Title: ")

        # 3. Quantity Logic
        while True:
            # Gathers user input and validates it
            raw_qty = input("Qty: ")
            clean_qty = input_defense.validate_int(raw_qty)
            if clean_qty:
                break
        # Adds the new book entry to the DB
        db.add_book(clean_id, title, clean_author_id, clean_qty)
        print(f"{Colors.GREEN}{Colors.BOLD}"
              f"Book added successfully!{Colors.END}")

    # Control flow for updating a book
    elif menu == "2":
        # 1. Book ID logic
        while True:
            # Gathers user input and validates it
            raw_id = input("Book ID to update: ")
            clean_id = input_defense.validate_four_digit_id(raw_id)
            if clean_id:
                break
        # 2. Column logic
        while True:
            # Gathers user input for column and validates it
            raw_column = input("Update Title, AuthorID, or Qty?: ").lower()
            clean_column = input_defense.validate_column(raw_column)
            if clean_column:
                break
        # Qty column logic
        if clean_column == "qty":
            while True:
                # Gathers user input and validates it
                new_value = input("Enter new quantity: ")
                clean_new_value = input_defense.validate_int(new_value)
                if clean_new_value is not None:
                    break
        # AuthorID column logic
        elif clean_column == "authorid":
            while True:
                # Gathers user input and validates it
                new_value = input("Enter new Author ID: ")
                clean_new_value = input_defense.validate_four_digit_id(
                    new_value)
                if clean_new_value:
                    # Checks if the user has entered a new author
                    if not db.author_exists(clean_new_value):
                        print(
                            f"{Colors.YELLOW}Author ID {clean_new_value} not "
                            f"found. Provide details:{Colors.END}")
                        # If it's a new author, gathers new author details
                        author_name = input("Author Name: ")
                        author_country = input("Author Country: ")
                        # Adds new author
                        db.add_author(clean_new_value,
                                      author_name, author_country)
                        print(f"{Colors.GREEN}New author added!{Colors.END}")
                    break
        else:
            # Title column logic
            clean_new_value = input("Enter new title: ")
        # Update the book
        db.update_book(clean_id, clean_column, clean_new_value)
        print(f"{Colors.GREEN}Update successful!{Colors.END}")

    # Control flow for deleting a book
    elif menu == "3":
        while True:
            # Gathers user input and validates it
            raw_id = input("Book ID to delete: ")
            clean_id = input_defense.validate_four_digit_id(raw_id)
            if clean_id:
                break
        # Deletes the book
        db.delete_book(clean_id)
        print(f"{Colors.RED}Book deleted successfully.{Colors.END}")

    # Control flow for searching for a book
    elif menu == "4":
        while True:
            # Gathers user input and validates it
            raw_id = input("Search Book ID: ")
            clean_id = input_defense.validate_four_digit_id(raw_id)
            if clean_id:
                break
        # Returns the book details from the DB
        book = db.get_book_details(clean_id)

        # Prints the book details
        if book:
            title, author_name, country = book
            print(f"\n{Colors.CYAN}Details{Colors.END}")
            print("-" * 50)
            print(f"Title: {title}")
            print(f"Author's Name: {author_name}")
            print(f"Author's Country: {country}")
            print("-" * 50)
        else:
            print(f"{Colors.RED}Error: Book ID not found.{Colors.END}")

    # Control flow for viewing all the books
    elif menu == "5":
        # Returns all the books from the DB
        books = db.view_all_books()
        # Prints all of the books
        if books:
            print(f"\n{Colors.CYAN}Inventory List{Colors.END}")
            for book in books:
                title, author_name, country = book
                print("-" * 50)
                print(f"Title: {title}")
                print(f"Author: {author_name}")
                print(f"Country: {country}")
            print("-" * 50)
        else:
            print(f"{Colors.YELLOW}No books in the database.{Colors.END}")

    # Program exit
    elif menu == "0":
        print(f"{Colors.BOLD}Exiting system...{Colors.END}")
        break
