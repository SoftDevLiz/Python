numbers = []

while True:

    number = int(input("Enter number (-1 to stop): "))

    if number == 0:
        print("Sorry, no 0's")
        continue

    if number == -1:
        break

    numbers.append(number)

if len(numbers) > 0:
    average = sum(numbers) / len(numbers)
    print(average)
else:
    print("No valid numbers entered.")
