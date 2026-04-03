import sqlite3


def init_db():
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
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = "INSERT INTO book(id, title, authorID, qty) \
                    VALUES(?, ?, ?, ?)"

        cursor.execute(sql_query, (id, title, author_id, qty))
        db.commit()


def update_book(id, column, new_value):
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = f"UPDATE book SET {column} = ? WHERE id = ?"

        cursor.execute(sql_query, (new_value, id))
        db.commit()


def get_book_details(id):
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = "SELECT book.title, author.name, author.country FROM book \
        INNER JOIN author ON book.authorID = author.id WHERE book.id = ?"

        cursor.execute(sql_query, (id,))
        return cursor.fetchone()


def view_all_books():
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = "SELECT book.title, author.name, author.country FROM book \
        INNER JOIN author ON book.authorID = author.id"

        cursor.execute(sql_query)
        return cursor.fetchall()


def delete_book(id):
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        sql_query = "DELETE FROM book WHERE id = ?"

        cursor.execute(sql_query, (id,))
        db.commit()


def book_exists(id):
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM book WHERE id = ?", (id,))
        return cursor.fetchone() is not None  # Returns True if found,
        # False if not


def author_exists(id):
    """Checks if the author ID exists in the author table."""
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM author WHERE id = ?", (id,))
        return cursor.fetchone() is not None  # Returns True if found,
        # False if not


def add_author(id, name, country):
    """Adds a new author to the author table."""
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO author(id, name, country) VALUES(?,?,?)",
                       (id, name, country))
        db.commit()
