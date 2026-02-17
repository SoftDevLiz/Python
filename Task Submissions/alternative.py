string = input("Gimme a sentence: ")

def jamble_letters(string):
    jambled_letters_string = ""

    for index, value in enumerate(string):

        if index % 2 == 0:
            modified_char = value.upper()
            jambled_letters_string += modified_char
        else:
            modified_char = value.lower()
            jambled_letters_string += modified_char
    
    return jambled_letters_string

letter_result = jamble_letters(string)

print(letter_result)

def jamble_words(string):
    word_list = string.split()
    jambled_word_list = []

    for index, value in enumerate(word_list):

        if index % 2 == 0:
            modified_word = value.upper()
            jambled_word_list.append(modified_word)
        else:
            modified_word = value.lower()
            jambled_word_list.append(modified_word)

    return " ".join(jambled_word_list)

word_result = jamble_words(string)

print(word_result)
    