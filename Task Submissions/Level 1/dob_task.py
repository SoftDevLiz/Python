# dob_task.py

with open("DOB.txt", "r") as file:
    print("Name")
    for line in file:
        line = line.strip()
        if line:
            name = " ".join(line.split()[:-3])
            print(name)

print("\nBirthdate")
with open("DOB.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            birthdate = " ".join(line.split()[-3:])
            print(birthdate)
