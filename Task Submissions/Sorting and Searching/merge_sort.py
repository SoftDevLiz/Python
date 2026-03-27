
# ===== Modified Merge Sort Algorithm =====

def merge_sort(items):
    items_length = len(items)
    temporary_storage = [None] * items_length
    size_of_subsections = 1

    while size_of_subsections < items_length:
        for i in range(0, items_length, size_of_subsections * 2):
            first_section_start = i
            first_section_end = min(i + size_of_subsections, items_length)
            second_section_start = first_section_end
            second_section_end = min(
                first_section_end + size_of_subsections, items_length)

            sections = (first_section_start,
                        first_section_end), (second_section_start,
                                             second_section_end)
            merge(items, sections, temporary_storage)

        size_of_subsections *= 2
    return items


def merge(items, sections, temporary_storage):
    (f_start, f_end), (s_start, s_end) = sections
    left_index, right_index, temp_index = f_start, s_start, 0

    while left_index < f_end and right_index < s_end:
        # Compare length and use >= for longest-to-shortest
        if len(items[left_index]) >= len(items[right_index]):
            temporary_storage[temp_index] = items[left_index]
            left_index += 1
        else:
            temporary_storage[temp_index] = items[right_index]
            right_index += 1
        temp_index += 1

    # Copy any remaining elements
    while left_index < f_end:
        temporary_storage[temp_index] = items[left_index]
        left_index += 1
        temp_index += 1
    while right_index < s_end:
        temporary_storage[temp_index] = items[right_index]
        right_index += 1
        temp_index += 1

    # Copy back to original list
    for i in range(temp_index):
        items[f_start + i] = temporary_storage[i]


# Example usage:
word_list = ["apple", "hi", "strawberry", "banana", "a"]
print(merge_sort(word_list))
