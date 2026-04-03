import database_logic as db
import validators as input_defense

db.init_db()

while True:

    menu = input('''
                1. Enter book
                2. Update book
                3. Delete book
                4. Search books
                5. View details of all books
                0. Exit
                ''')

    if menu == "1":
        while True:
            raw_author_id = input("Author ID: ")
            clean_author_id = input_defense.validate_four_digit_id(
                raw_author_id)
            if clean_author_id:

                if not db.author_exists(clean_author_id):
                    print(
                        f"Author ID {clean_author_id} not found. "
                        "Please provide details:")
                    author_name = input("Author Name: ")
                    author_country = input("Author Country: ")
                    db.add_author(clean_author_id, author_name, author_country)
                    print("New author added successfully.")
                    break
                else:
                    break
        while True:
            raw_id = input("Book ID: ")
            clean_id = input_defense.validate_four_digit_id(raw_id)

            if clean_id:
                # Check if it exists in DB [cite: 1151]
                if db.book_exists(clean_id):
                    print(f"Error: Book ID {clean_id} already exists!")
                else:
                    break  # ID is valid and unique, move on

            # 3. Get Title
        title = input("Title: ")

        # 4. Get and validate Quantity
        while True:
            raw_qty = input("Qty: ")
            clean_qty = input_defense.validate_int(raw_qty)
            if clean_qty:  # Ensure 0 is accepted as a valid qty
                break

            db.add_book(clean_id, title, clean_author_id, clean_qty)
            print("Book added successfully!")

    elif menu == "2":
        while True:
            raw_id = input("Book ID: ")
            clean_id = input_defense.validate_four_digit_id(raw_id)
            if clean_id:
                break

        while True:
            raw_column = input(
                "Would you like to update the "
                "Title, AuthorID, or Qty?: ").lower()
            clean_column = input_defense.validate_column(raw_column)
            if clean_column:
                break

        if clean_column == "qty":
            while True:
                new_value = input("Update new value: ")
                clean_new_value = input_defense.validate_int(new_value)
                if clean_new_value:
                    break
        elif clean_column == "authorid":
            while True:
                new_value = input("Author ID: ")
                clean_new_value = input_defense.validate_four_digit_id(
                    new_value)
                if clean_new_value:

                    if not db.author_exists(clean_new_value):
                        print(
                            f"Author ID {clean_new_value} not found. "
                            "Please provide details:")
                        author_name = input("Author Name: ")
                        author_country = input("Author Country: ")
                        db.add_author(clean_new_value,
                                      author_name, author_country)
                        print("New author added successfully and "
                              "book updated!")
                        break
                    else:
                        break
        else:
            clean_new_value = input("Update new value: ")

        db.update_book(clean_id, clean_column, clean_new_value)

    elif menu == "3":
        while True:
            raw_id = input("Book ID: ")
            clean_id = input_defense.validate_four_digit_id(raw_id)
            if clean_id:
                break

        db.delete_book(clean_id)

    elif menu == "4":
        while True:
            raw_id = input("Book ID: ")
            clean_id = input_defense.validate_four_digit_id(raw_id)
            if clean_id:
                break

        book = db.get_book_details(clean_id)
        if book:
            # Unpacking the tuple
            title, author_name, country = book

            print("\nDetails")
            print("-" * 50)  # Prints a line of 50 dashes
            print(f"Title: {title}")
            print(f"Author's Name: {author_name}")
            print(f"Author's Country: {country}")
            print("-" * 50)
        else:
            print("Error: Book ID not found.")

    elif menu == "5":
        books = db.view_all_books()
        if books:
            print("\nDetails")
            for book in books:

                title, author_name, country = book

                print("-" * 50)  # Prints a line of 50 dashes
                print(f"Title: {title}")
                print(f"Author's Name: {author_name}")
                print(f"Author's Country: {country}")
                print("-" * 50)
        else:
            print("No books in the database.")
    elif menu == "0":
        print("Exiting...")
        break

# TODO:
# User feedback
# Bug: when adding a new book and typing in "ten", it proceeds to add the book?
