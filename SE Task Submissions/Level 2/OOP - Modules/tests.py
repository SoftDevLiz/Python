import unittest
from unittest.mock import patch, MagicMock
from models import UserService, TaskService


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Arrange: Initialize the services before each test."""
        self.user_service = UserService()
        self.task_service = TaskService()

    @patch('models.get_db_connection')
    def test_authenticate_success(self, mock_conn):
        """Use Case 1: Testing successful user login."""
        # Arrange: Mock the database to return a 'user' object
        mock_db = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.execute.return_value.fetchone.return_value = {
            'username': 'admin'}

        # Act: Attempt to authenticate
        result = self.user_service.authenticate('admin', 'password')

        # Assert: Verify the result is True
        self.assertTrue(result)

    @patch('models.get_db_connection')
    def test_register_user_duplicate(self, mock_conn):
        """Use Case 2: Testing registration failure for existing user."""
        import sqlite3
        # Arrange: Force the database to raise an IntegrityError (duplicate primary key)
        mock_db = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.execute.side_effect = sqlite3.IntegrityError

        # Act: Attempt to register a duplicate name
        result = self.user_service.register('admin', 'newpassword')

        # Assert: Verify the service returns False
        self.assertFalse(result)

    @patch('models.get_db_connection')
    def test_add_task_logic(self, mock_conn):
        """Use Case 3: Testing task creation logic."""
        # Arrange
        mock_db = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_db

        # Act: Add a task
        self.task_service.add_task(
            'user1', 'Test Title', 'Test Desc', '05 Apr 2026', '10 Apr 2026')

        # Assert: Verify the SQL execute was called exactly once
        self.assertEqual(mock_db.execute.call_count, 1)

    @patch('models.get_db_connection')
    def test_get_user_tasks_empty(self, mock_conn):
        """Use Case 4: Testing retrieval when a user has no tasks."""
        # Arrange: Mock database to return an empty list
        mock_db = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.execute.return_value.fetchall.return_value = []

        # Act
        tasks = self.task_service.get_user_tasks('new_user')

        # Assert: Verify the list is empty
        self.assertEqual(len(tasks), 0)


if __name__ == '__main__':
    unittest.main()
