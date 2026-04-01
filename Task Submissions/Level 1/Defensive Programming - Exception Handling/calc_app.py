
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by 0")
    return a / b


def get_numbers():
    a = int(input("First number: "))
    b = int(input("Second number: "))
    return a, b


def validate_numbers(a, b):
    try:
        return float(a), float(b)
    except ValueError:
        raise ValueError("Only numbers allowed good sir! Try again!")


def get_operator():
    operator = input("Operator (+, -, *, or /): ")
    return operator


def validate_operator(operator):
    if operator not in OPERATORS:
        raise ValueError("Only specified operators allowed (+, -, *, /)")
    return operator


def user_choice():
    choice = input("Would you like to view all previous equations? y/n ")
    return choice


def validate_choice(choice):
    choices = ['y', 'n']

    if choice not in choices:
        raise ValueError("Please type in only 'y' or 'n'")
    return choice


def write_to_file():
    with open('equations.txt', 'a') as file:
        file.write(f"{a} {operator} {b} = {result}\n")


def read_file():
    with open('equations.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            print(line)


OPERATORS = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }


while True:

    try:
        a, b = get_numbers()
        a, b = validate_numbers(a, b)

        operator = get_operator()
        operator = validate_operator(operator)

        result = OPERATORS[operator](a, b)
        print(f"{a} {operator} {b} is {result}!")

        write_to_file()

        choice = user_choice()
        choice = validate_choice(choice)

        if choice == 'y':
            read_file()
        else:
            print("Okay! Goodbye!")

        break
    except ValueError as e:
        print(e)
