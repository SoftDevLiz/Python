user_temp = input("temp?")
user_unit = input("C or F?")

def c_to_f(temp):
    return (temp * 1.8) + 32

def f_to_c(temp):
    return (temp - 32) / 1.8

try:
    temp = float(user_temp)
    unit = user_unit.lower()

    if unit == "c":
        result = c_to_f(temp)
        print(f"{temp} Celsius is {result} Fahrenheit")
    elif unit == "f":
        result = f_to_c(temp)
        print(f"{temp} Fahrenheit is {result} Celsius")
    else:
        print("Invalid temp unit. Please type only 'c' or 'f'.")

except:
    print("Please use numerical characters as your temperature")
