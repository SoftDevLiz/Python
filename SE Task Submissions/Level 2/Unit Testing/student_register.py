def validate_student_id(id_input):
    """Validates that the student ID is a number."""
    try:
        return int(id_input)
    except ValueError:
        raise ValueError("Student ID must be numerical")


def format_reg_entry(student_id):
    """Formats the ID for the registration form."""
    return f"{student_id} \n" + "**********\n"


def main():
    id_list = []
    while True:
        try:
            student_qty = int(input('Enter the amount of students: '))
            break
        except ValueError:
            print("Please enter a numerical character")

    for _ in range(student_qty):
        while True:
            try:
                student_id = input('Student ID: ')
                id_list.append(validate_student_id(student_id))
                break
            except ValueError as e:
                print(e)

    with open('reg_form.txt', 'w+') as file:
        for student in id_list:
            file.write(format_reg_entry(student))

    print('registration complete! check the reg_form!')


if __name__ == "__main__":
    main()
