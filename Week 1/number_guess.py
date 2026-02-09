import random

answer = random.randint(1, 100)

def ask_user():
    user_guess = input("guess the number between 1-100? ")
    user_guess = int(user_guess)
    return user_guess

user_guess = ask_user()
attempts = 0

while user_guess != answer:
    attempts += 1

    if user_guess > answer:
        print("Too high. Guess lower! ")
        user_guess = ask_user()
    elif user_guess < answer:
        print("Too low. Try higher! ")
        user_guess = ask_user()

print(f"You did it! The answer is {answer} and it took you {attempts} attempts!")