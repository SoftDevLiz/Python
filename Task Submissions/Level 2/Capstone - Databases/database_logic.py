import sqlite3


def init_db():
    """
    Initializes the ebookstore database by creating the 'book' and 'author'
    tables if they do not exist and populating them with default values.
    """
    try:
        # 1. Connect and create cursor
        with sqlite3.connect("ebookstore.db") as db:

            cursor = db.cursor()

            # 2. Create the table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS book(
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    authorID INTEGER,
                    qty INTEGER)
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS author(
                id INTEGER PRIMARY KEY,
                name TEXT,
                country TEXT)
        ''')

            # 3. Insert rows

            book = [
                (3001, "A Tale of Two Cities", 1290, 30),
                (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
                (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
                (3004, "The Lord of the Rings", 6380, 37),
                (3005, "Alice’s Adventures in Wonderland", 5620, 12)
            ]

            author = [
                (1290, "Charles Dickens", "England"),
                (8937, "J.K. Rowling", "England"),
                (2356, "C.S. Lewis", "Ireland"),
                (6380, "J.R.R. Tolkien", "South Africa"),
                (5620, "Lewis Carroll", "England")
            ]

            cursor.executemany('''INSERT OR IGNORE INTO
                                book(id, title, authorID, qty)
                                VALUES(?,?,?,?)''', book)

            cursor.executemany('''INSERT OR IGNORE INTO
                                author(id, name, country)
                                VALUES(?,?,?)''', author)

            db.commit()

    except Exception as e:
        db.rollback()  # Undo changes if there's an error
        print(f"An error occurred: {e}")


def add_book(id, title, author_id, qty):
    """
    Inserts a new book record into the book table.

    Args:
        id (int): The unique 4-digit ID for the book.
        title (str): The title of the book.
        author_id (int): The ID of the author (foreign key).
        qty (int): The quantity of books in stock.
    """
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = "INSERT INTO book(id, title, authorID, qty) \
                    VALUES(?, ?, ?, ?)"

        cursor.execute(sql_query, (id, title, author_id, qty))
        db.commit()


def update_book(id, column, new_value):
    """
    Updates a specific attribute of a book record using
    dynamic column selection.

    Args:
        id (int): The ID of the book to update.
        column (str): The column name to be updated (e.g., 'title', 'qty').
        new_value (obj): The new data to be saved to the specified column.
    """
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = f"UPDATE book SET {column} = ? WHERE id = ?"

        cursor.execute(sql_query, (new_value, id))
        db.commit()


def get_book_details(id):
    """
    Retrieves the title, author name, and country for a specific book ID.

    Args:
        id (int): The ID of the book to search for.
    Returns:
        tuple: (title, author_name, country) if found, otherwise None.
    """
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = "SELECT book.title, author.name, author.country FROM book \
        INNER JOIN author ON book.authorID = author.id WHERE book.id = ?"

        cursor.execute(sql_query, (id,))
        return cursor.fetchone()


def view_all_books():
    """
    Retrieves detailed information for all books in the inventory,
    joining with the author table for complete metadata.

    Returns:
        list: A list of tuples containing (title, author_name, country).
    """
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = "SELECT book.title, author.name, author.country FROM book \
        INNER JOIN author ON book.authorID = author.id"

        cursor.execute(sql_query)
        return cursor.fetchall()


def delete_book(id):
    """
    Permanently removes a book record from the database based on its ID.

    Args:
        id (int): The ID of the book to be deleted.
    """
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = "DELETE FROM book WHERE id = ?"

        cursor.execute(sql_query, (id,))
        db.commit()


def book_exists(id):
    """
    Checks if a specific book ID already exists in the book table.

    Args:
        id (int): The ID to check.
    Returns:
        bool: True if the ID exists, False otherwise.
    """
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM book WHERE id = ?", (id,))
        return cursor.fetchone() is not None  # Returns True if found,
        # False if not


def author_exists(id):
    """
    Checks if a specific author ID exists in the author table to maintain
    referential integrity.

    Args:
        id (int): The author ID to check.
    Returns:
        bool: True if the author exists, False otherwise.
    """
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM author WHERE id = ?", (id,))
        return cursor.fetchone() is not None  # Returns True if found,
        # False if not


def add_author(id, name, country):
    """
    Inserts a new author record into the author table.

    Args:
        id (int): The unique 4-digit ID for the author.
        name (str): The name of the author.
        country (str): The author's country of origin.
    """
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO author(id, name, country) VALUES(?,?,?)",
                       (id, name, country))
        db.commit()
