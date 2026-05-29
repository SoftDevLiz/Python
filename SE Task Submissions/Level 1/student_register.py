id_list = []

while True:
    try:
        student_qty = input('Enter the amount of students: ')
        student_qty = int(student_qty)
        break
    except ValueError:
        print("Please enter a numerical character")

for _ in range(student_qty):
    while True:
        try:
            student_id = input('Student ID: ')
            id_list.append(int(student_id))
            break
        except ValueError:
            print('Student ID cannot contain letters')

with open('reg_form.txt', 'w+') as file: 
    for student in id_list:
        file.write(f'{student} \n' + '**********\n')

print('registration complete! check the reg_form!')