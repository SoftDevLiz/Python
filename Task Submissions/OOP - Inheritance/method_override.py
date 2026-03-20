# ----- CLASSES ----- #

# Parent class
class Adult():
    # Constructor that makes places for attributes
    def __init__(self, name, age, eye_colour, hair_colour):
        self.name = name
        self.age = age
        self.eye_colour = eye_colour
        self.hair_colour = hair_colour

    # Method that prints out someone of the 'Adult' class
    # is old enough to drive
    def can_drive(self):
        print(f"\n{self.name} is old enough to drive")


# Subclass
class Child(Adult):
    # Constructor that makes places for attributes
    def __init__(self, name, age, eye_colour, hair_colour):
        # Use super to gain access to parent class methods
        super().__init__(name, age, eye_colour, hair_colour)

    # Method that prints out someone of the 'Child' subclass
    # is too young to drive
    def can_drive(self):
        print(f"\n{self.name} is too young to drive")


# ----- INPUTS ----- #

print("\nHi! Please enter a few details about yourself:\n")

while True:
    """Gather all inputs within a try/except
        to catch any input errors for age"""
    try:
        name = input("Name: ")
        age = int(input("Age: "))
        hair_col = input("Hair colour: ")
        eye_col = input("Eye colour: ")

        """Checks if they are 18 or older and creates either an Adult or Child
            person object based on the check"""
        if age >= 18:
            person = Adult(name, age, eye_col, hair_col)
        else:
            person = Child(name, age, eye_col, hair_col)

        # Calls the method on the object
        person.can_drive()
        break
    except ValueError:
        print("Use numbers to enter age :)")
