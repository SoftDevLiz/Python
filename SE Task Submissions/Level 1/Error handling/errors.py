# Fixed Syntax Error:
# The original print statements were missing parentheses.
print("Welcome to the error program")

# Fixed Syntax Error:
# The original line had incorrect indentation.
print("\n")


# Fixed Syntax Error:
# The variable used '==' instead of '=' for assignment.
# Fixed Runtime Error:
# "24 years old" could not be converted to an integer,
# so only the number "24" was stored as a string.
age_str = "24"

# Convert the string to an integer.
age = int(age_str)

# Fixed Runtime Error:
# Cannot concatenate a string and integer directly,
# so an f-string was used instead.
print(f"I'm {age} years old.")


# Fixed Logical Error:
# The original code stored "3" as a string,
# which cannot be added to an integer.
years_from_now = 3

# Add the future years to the current age.
total_years = age + years_from_now

# Fixed Logical Error:
# The original code printed "answer_years" as text
# instead of printing the variable value.
print(f"The total number of years: {total_years}")


# Fixed Runtime Error:
# The variable name 'total' did not exist.
# Changed it to 'total_years'.
total_months = total_years * 12

# Fixed Logical Error:
# The task mentions 3 years and 6 months,
# so 6 months were added to the calculation.
print(f"In 3 years and 6 months, I'll be {total_months + 6} months old")
