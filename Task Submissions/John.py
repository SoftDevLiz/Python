names = []

while True:
    user_input = input('Enter name: ').lower()

    if user_input == 'john':
        print(names)
        break
    else:
        names.append(user_input)