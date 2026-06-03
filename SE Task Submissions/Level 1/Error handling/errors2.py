# Fixed Syntax Error:
# The original code used Lion without quotes, which caused a NameError
# because Python treated it as a variable instead of a string.
animal = "lion"

animal_type = "cub"
number_of_teeth = 16


# Fixed Syntax Error:
# The original string was not formatted correctly (no f-string used),
# so placeholders like {animal} would not be replaced.

# Fixed Logical Error:
# The original sentence structure was incorrect:
# - "It is a {number_of_teeth}" didn't make sense grammatically.
# Reordered and corrected wording.
full_spec = f"This is a {animal}. It is a {animal_type} and it has {number_of_teeth} teeth."


# Fixed Syntax Error:
# print was missing parentheses (Python 3 requirement)
print(full_spec)
