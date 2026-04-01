import random

# Dictionary of jokes

jokes = {
 "Why don’t skeletons fight each other?": "Because they don’t have the guts.",
 "I told my computer I needed a break…": "Now it won't stop sending me KitKat ads...",
 "Why did the scarecrow win an award?": "Because he was outstanding in his field."
 }

# jokes.items() gives me key, value pairs
# list converts the dict into something indexable for random choice
# random.choice() picks one pair

joke, punchline = random.choice(list(jokes.items()))

print(joke)
input("Press Enter for the punchline...")
print(punchline)