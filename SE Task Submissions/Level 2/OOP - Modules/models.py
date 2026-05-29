import sqlite3
from database import get_db_connection


class TaskService:
    def add_task(self, user, title, desc, assigned, due):
        """Saves a new task to the database."""
        with get_db_connection() as conn:
            conn.execute("""INSERT INTO tasks (username, title, description,
                            assigned_date, due_date, completed)
                            VALUES (?, ?, ?, ?, ?, 'No')""",
                         (user, title, desc, assigned, due))
            conn.commit()

    def get_user_tasks(self, username):
        """Retrieves tasks assigned to a specific user."""
        with get_db_connection() as conn:
            return conn.execute("SELECT * FROM tasks WHERE username = ?", (username,)).fetchall()

    def get_all_tasks(self):
        """Retrieves every task in the system."""
        with get_db_connection() as conn:
            return conn.execute("SELECT * FROM tasks").fetchall()

    def mark_complete(self, task_id):
        """Updates a task status to Yes."""
        with get_db_connection() as conn:
            conn.execute(
                "UPDATE tasks SET completed = 'Yes' WHERE id = ?", (task_id,))
            conn.commit()


class UserService:
    def authenticate(self, username, password):
        """Checks login credentials."""
        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                                (username, password)).fetchone()
            return user is not None

    def register(self, username, password):
        """Registers a new user if the name isn't taken."""
        try:
            with get_db_connection() as conn:
                conn.execute("INSERT INTO users VALUES (?, ?)",
                             (username, password))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
