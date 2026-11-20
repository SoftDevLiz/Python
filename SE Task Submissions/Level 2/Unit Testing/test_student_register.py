import unittest
# Importing the functions from your implementation file
from student_register import validate_student_id, format_reg_entry


class TestStudentRegister(unittest.TestCase):

    def test_valid_id_input(self):
        """
        Scenario 1: Testing if a valid numerical string
        is converted to int.
        """
        # Arrange
        id_input = "12345"
        # Act
        result = validate_student_id(id_input)
        # Assert
        self.assertEqual(result, 12345)

    def test_invalid_id_input(self):
        """Scenario 2: Testing if non-numerical input raises a ValueError."""
        # Arrange
        id_input = "ABC"
        # Act & Assert
        with self.assertRaises(ValueError):
            validate_student_id(id_input)

    def test_format_reg_entry(self):
        """
        Scenario 3: Testing if the output string
        matches the required format.
        """
        # Arrange
        student_id = 999
        expected_output = "999 \n**********\n"
        # Act
        result = format_reg_entry(student_id)
        # Assert
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
