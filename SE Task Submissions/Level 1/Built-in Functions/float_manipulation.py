import statistics

# -----------------------------
# Store valid float inputs
# -----------------------------
user_floats = []

# -----------------------------
# Collect exactly 10 VALID float inputs
# (invalid inputs do NOT count)
# -----------------------------
while len(user_floats) < 10:
    try:
        value = float(input(f"Enter float {len(user_floats) + 1}: "))
        user_floats.append(value)

    except ValueError:
        print("Words aren't floats! Try again.\n")


# -----------------------------
# Show collected values
# -----------------------------
print(f"\nCollected values: {user_floats}\n")


# -----------------------------
# The total
# -----------------------------
total = sum(user_floats)
print(f"The total is {total}\n")


# -----------------------------
# Find max and min values + indexes
# -----------------------------
max_value = max(user_floats)
min_value = min(user_floats)

max_index = user_floats.index(max_value)
min_index = user_floats.index(min_value)

print(f"Index of max is {max_index}")
print(f"Index of min is {min_index}\n")


# -----------------------------
# Statistical calculations
# -----------------------------
mean_value = statistics.mean(user_floats)
median_value = statistics.median(user_floats)

print(f"The average is {mean_value:.2f}")
print(f"The median is {median_value}\n")
