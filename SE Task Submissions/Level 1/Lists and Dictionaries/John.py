# List to store all entered names
names = []


# -----------------------------
# Input loop for collecting names
# -----------------------------
while True:

    # Get user input and standardise it to lowercase
    user_input = input('Enter name: ').lower()

    # -----------------------------
    # Sentinel value check (stop condition)
    # -----------------------------
    if user_input == 'john':
        # "john" is used as a trigger to stop input collection
        print(f"Incorrect names: {names}")
        break

    else:
        # Add valid names to the list
        names.append(user_input)
