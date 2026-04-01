import statistics

i = 0

user_floats = []

while i < 3:
    try:    
        user_floats.append(float(input("Give me a float: ")))
        i += 1
    except ValueError:
        print("Words aren't floats!")

print(user_floats)

total = sum(user_floats)

print(f"The total is {total}")

max_value = max(user_floats)
max_index = user_floats.index(max_value)
min_value = min(user_floats)
min_index = user_floats.index(min_value)
print(f"Index of max is {max_index} and index of min is {min_index}")

mean_value = statistics.mean(user_floats)
print(f'The avg is {mean_value}')

median_value = statistics.median(user_floats)
print(f'The median is {median_value}')
