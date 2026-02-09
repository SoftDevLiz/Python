import string

sentence = input("give the pomputer a sentence to analyze: ")
sentence = sentence.lower()

clean_sentence = ""

for char in sentence:
    if char not in string.punctuation:
        clean_sentence += char

vowels = ['a', 'e', 'i', 'o', 'u']

# Counts number of words
word_list = clean_sentence.split()
list_len = len(word_list)

# Finds longest words
longest_word = max(word_list, key=len)

# Counts number of vowels in sentence
vowel_amount = 0

for letter in clean_sentence:

    if letter in vowels:
        vowel_amount += 1

print(f"Your sentence has {list_len} words and {vowel_amount} vowels. The longest word is {longest_word}.")