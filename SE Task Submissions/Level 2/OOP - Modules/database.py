import sqlite3


def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('task_manager.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def init_db():
    """Creates the necessary tables if they don't already exist."""
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                        (username TEXT PRIMARY KEY, password TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT, title TEXT, description TEXT,
                         assigned_date TEXT, due_date TEXT, completed TEXT,
                         FOREIGN KEY (username)
                         REFERENCES users (username))''')
        # Create default admin if not exists
        conn.execute(
            "INSERT OR IGNORE INTO users VALUES ('admin', 'adm1n')")
