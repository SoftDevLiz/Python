students = {
    "Alice": [78, 85, 90],
    "Ben": [65, 70, 72],
    "Cara": [88, 92, 95],
    "Daniel": [55, 60, 58],
    "Eva": [91, 89, 94]
}

# name should always be a string, grades should always be a list
def add_student(name, grades):
    students[name] = grades

add_student("Liz", [1, 2, 3])

print(students)

# name should always be a string, grades should always be a list
def update_grades(name, grades):
    students[name] = grades

update_grades("Liz", [60, 85, 100])

print(students)

# name should always be a string 
def student_avg(name):
    student_grades = students[name]
    amount_of_grades = len(student_grades)
    sum_of_grades = 0

    for grade in student_grades:
        sum_of_grades = sum_of_grades + grade

    return sum_of_grades / amount_of_grades

avg = student_avg("Liz")

print(avg)

def find_top_student(student_data):
    avg_grades = {}

    for student in student_data:
        avg = student_avg(student)
        avg_grades[student] = avg

    top_student = max(avg_grades, key=avg_grades.get)
    top_grade = avg_grades[top_student]

    return top_student, top_grade

top_student = find_top_student(students)

print(top_student)