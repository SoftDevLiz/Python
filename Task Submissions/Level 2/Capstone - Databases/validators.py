COLUMNS = ['title', 'authorid', 'qty']


def validate_four_digit_id(user_input):
    """Checks if input is a 4-digit integer."""
    try:
        # Check if it's a number
        id = int(user_input)
        # Check the length by converting back to string
        if len(str(user_input)) == 4:
            return id
        else:
            print("Error: ID must be exactly 4 digits.")
            return None
    except ValueError:
        print("Error: Please enter a valid 4 digit ID.")
        return None


def validate_column(user_input):
    if user_input in COLUMNS:
        return user_input
    else:
        print("Error: Please enter a valid column name.")
        return None


def validate_int(user_input):
    try:
        qty = int(user_input)
        return qty
    except ValueError:
        print("Error: Please enter numerical characters.")
        return None
