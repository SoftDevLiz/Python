int_list = [2, 4, 6, 8, 10, 12]


def adding_up_to(int_list, index):
    '''
    Takes a list of integers and an index then
    sums all integers up until the given index
    '''

    # Base case - we know that if the index is 0
    # the total would simply be the integer in index 0
    if index == 0:
        return int_list[0]
    # Recursion - we add together the integer at the given index
    # with the integer at the previous index by calling the function again
    else:
        return int_list[index] + adding_up_to(int_list, index - 1)


result = adding_up_to(int_list, 2)

print(result)
