friends_names = ["Jevan", "Ruan", "Melissa"]

print(friends_names[0], friends_names[-1], len(friends_names))

friends_ages = ["25", "30", "32"]

for i, friend in enumerate(friends_names):
    print(f"{friends_names[i]} is {friends_ages[i]} years old")
