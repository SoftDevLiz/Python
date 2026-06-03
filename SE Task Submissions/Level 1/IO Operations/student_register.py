# List to store all student IDs
id_list = []


# -----------------------------
# Get number of students
# -----------------------------
while True:
    try:
        student_qty = input('Enter the amount of students: ')

        # Convert input to integer (must be numeric)
        student_qty = int(student_qty)
        break

    except ValueError:
        # Handles non-numeric input (runtime error prevention)
        print("Please enter a numerical character")


# -----------------------------
# Collect student IDs
# -----------------------------
for _ in range(student_qty):

    while True:
        try:
            student_id = input('Student ID: ')

            # Convert ID to integer to ensure it contains only numbers
            id_list.append(int(student_id))
            break

        except ValueError:
            # Handles letters or invalid input (runtime error prevention)
            print('Student ID cannot contain letters')


# -----------------------------
# Write registration form to file
# -----------------------------
with open('reg_form.txt', 'w+') as file:

    # Header for the register form
    file.write("Sign for attendance:\n\n")

    # Loop through each student ID
    for student in id_list:

        # Write the student ID line
        file.write(f"ID {student}\n")

        # Provide a blank line for student signature
        file.write("Signature: ______________________________\n")

        # Add a separator line for readability between entries
        file.write("-" * 40 + "\n")


# -----------------------------s
# Completion message
# -----------------------------
print('Registration complete! Check the reg_form file.')
