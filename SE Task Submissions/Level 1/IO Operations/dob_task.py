# dob_task.py

# Open the file in read mode
# First pass: extract and print names only
with open("DOB.txt", "r") as file:

    print("\nName")

    # Loop through each line in the file
    for line in file:

        # Remove trailing newline characters and extra spaces
        line = line.strip()

        # Skip empty lines to avoid errors
        if line:

            # Split the line into parts
            # Assume last 3 parts are the date of birth
            name = " ".join(line.split()[:-3])

            # Print only the name portion
            print(name)


# Open the file again for a second pass
# Second pass: extract and print birth dates only
with open("DOB.txt", "r") as file:

    print("\nBirth dates")

    for line in file:

        line = line.strip()

        if line:

            # Extract the last 3 elements as the birthdate
            birthdate = " ".join(line.split()[-3:])

            # Print only the birthdate portion
            print(birthdate)
