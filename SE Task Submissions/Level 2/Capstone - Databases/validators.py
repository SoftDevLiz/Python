# ANSI escape codes for clear user feedback
class Colors:
    RED = '\033[91m'
    END = '\033[0m'


# Valid columns for dynamic book update logic
COLUMNS = ['title', 'authorid', 'qty']


def validate_four_digit_id(user_input):
    """
    Validates that a user-provided ID is a four-digit integer.

    Args:
        user_input (str): The raw input from the clerk.
    Returns:
        int: The validated ID if successful, otherwise None.
    """
    try:
        # Convert to integer to ensure it's numerical
        val_id = int(user_input)
        # Check that the length is exactly 4 characters
        if len(str(user_input)) == 4:
            return val_id
        else:
            print(f"{Colors.RED}Error: ID must be exactly 4 digits."
                  f"{Colors.END}")
            return None
    except ValueError:
        print(
            f"{Colors.RED}Error: Please enter a valid 4-digit numerical ID."
            f"{Colors.END}")
        return None


def validate_column(user_input):
    """
    Validates that the provided column name matches the allowed update fields.

    Args:
        user_input (str): The column name entered by the user.
    Returns:
        str: The validated column name if valid, otherwise None.
    """
    if user_input in COLUMNS:
        return user_input
    else:
        print(
            f"{Colors.RED}Error: Please enter a valid column "
            f"(Title, AuthorID, or Qty).{Colors.END}")
        return None


def validate_int(user_input):
    """
    Validates that a user-provided input is a valid integer.

    Args:
        user_input (str): The raw input (e.g., quantity).
    Returns:
        int: The validated integer if successful, otherwise None.
    """
    try:
        qty = int(user_input)
        return qty
    except ValueError:
        print(f"{Colors.RED}Error: Please enter numerical characters only."
              f"{Colors.END}")
        return None
