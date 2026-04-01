import sqlite3

try:
    # 1. Connect and create cursor
    db = sqlite3.connect("python_programming.db")
    cursor = db.cursor()

    # 2. Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS python_programming(
            id INTEGER PRIMARY KEY,
            name TEXT,
            grade INTEGER
        )
    ''')

    # 3. Insert rows
    students = [
        (55, 'Carl Davis', 61),
        (66, 'Dennis Fredrickson', 88),
        (77, 'Jane Richards', 78),
        (12, 'Peyton Sawyer', 45),
        (2, 'Lucas Brooke', 99)
    ]

    cursor.executemany('''INSERT INTO python_programming(id, name, grade)
                          VALUES(?,?,?)''', students)

    # 4. Select records between 60 and 80
    cursor.execute('''SELECT * FROM python_programming
                   WHERE grade BETWEEN 60 AND 80''')

    print("Students with grades between 60 and 80:")
    for row in cursor.fetchall():
        print(row)

    # 5. Change Carl Davis's grade to 65
    cursor.execute('''UPDATE python_programming
                    SET grade = 65 WHERE name = 'Carl Davis' ''')

    # 6. Delete Dennis Fredrickson [cite: 1397]
    cursor.execute('''DELETE FROM python_programming
                   WHERE name = 'Dennis Fredrickson' ''')

    # 7. Change grade to 80 for all IDs > 55
    cursor.execute('''UPDATE python_programming
                    SET grade = 80 WHERE id > 55''')

    # Final step: Commit all changes
    db.commit()

except Exception as e:
    db.rollback()   # Undo changes if there's an error
    print(f"An error occurred: {e}")

finally:
    db.close()  # Always close the connection
