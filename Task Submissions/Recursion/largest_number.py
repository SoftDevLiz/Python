int_list = [5, 10, 15, 20, 25]


def largest_number(int_list):
    '''
    Takes a list of integers and returns the largest integer via recursion
    '''

    # Base case - if the length of the list is 1 then
    # we know the largest integer in the list is that single one
    if len(int_list) == 1:
        return int_list[0]

    # Recursion - We call the function again to look at
    # the rest of the list (index 1 and onwards)
    largest_of_rest = largest_number(int_list[1:])

    # Comparison between the first index integer
    # and the largest integer of the rest.
    # Returns whichever is largest.
    if int_list[0] > largest_of_rest:
        return int_list[0]
    else:
        return largest_of_rest


result = largest_number(int_list)

print(result)
