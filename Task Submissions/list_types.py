friends_names = ["Jevan", "Ruan", "Melissa"]

def return_last_index(list):
    return len(list) - 1

last_index = return_last_index(friends_names)

print(friends_names[0], friends_names[last_index], last_index)

friends_ages = ["25", "30", "32"]

print(f"{friends_names[0]} is {friends_ages[0]} years old")