str_manip = input("Enter any sentence: ")

last_letter = str_manip[-1]

print(str_manip.replace(last_letter, "@"))

print(str_manip[-3:][::-1])

first_three = str_manip[:3]
last_two = str_manip[-2:]
odd_word = first_three + last_two

print(odd_word.strip())
