int_list = [27, -3, 4, 5, 35, 2, 1, -40, 7, 18, 9, -1, 16, 100]

# ===== Linear Search =====
# It is the most straightforward approach for our small and unsorted list


def linear_search(target, int_list):

    for index in range(len(int_list)):
        if int_list[index] == target:
            return index


linear_search_result = linear_search(9, int_list)

print(f"\n9 can be found at index {linear_search_result}")

# ===== Insertion Sort =====


def insertion_sort(int_list):

    for i in range(1, len(int_list)):
        key = int_list[i]
        j = i - 1

        while j >= 0 and int_list[j] > key:
            int_list[j + 1] = int_list[j]
            j -= 1

        int_list[j + 1] = key

    return int_list


insertion_sort_result = insertion_sort(int_list)

print(
    f"\nThis was sorted by a Insertion Sort algorithm: "
    f"{insertion_sort_result}")

# ===== Binary Search =====
'''
 I chose this to practice the other most common search algorithm.

 It requires the data to be pre-sorted and
 it's the most efficient in terms of database size and speed.

 In the real world I would apply it for quickly looking up a user ID
 in a large database.
'''


def binary_search(target, int_list):
    low = 0
    high = len(int_list) - 1

    while low <= high:
        mid = (low + high) // 2

        if int_list[mid] == target:
            return mid

        if int_list[mid] > target:
            high = mid - 1

        if int_list[mid] < target:
            low = mid + 1

    print("The target number is not in this list.")
    return -1


binary_search_result = binary_search(9, insertion_sort_result)

print(f"\n9 can be found at index {binary_search_result}")
