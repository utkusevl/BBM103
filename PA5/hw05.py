import os


# Custom pseudorandom number generator with a random initial seed
class PRNG:
    def __init__(self, seed=None):
        # Use a truly random seed if no seed is provided
        if seed is None:
            seed = int.from_bytes(os.urandom(4), 'big')  # Generate a random 32-bit integer
        self.state = seed

    def randint(self, low, high):
        # Simple linear congruential generator (LCG)
        self.state = (1103515245 * self.state + 12345) % (2 ** 31)
        return low + (self.state % (high - low + 1))


# Generate logistics dataset
def generate_logistics_dataset(num_warehouses=100, max_packages=1000, seed=None):
    """Generates a logistics dataset with a random or specified seed."""
    prng = PRNG(seed)  # Initialize PRNG with the seed or a random one
    data = []
    for i in range(1, num_warehouses + 1):
        warehouse_id = f"WH-{str(i).zfill(3)}"
        priority_level = prng.randint(1, 5)
        package_count = prng.randint(0, max_packages)
        data.append([warehouse_id, priority_level, package_count])
    return data


# Save dataset to a CSV file
def save_to_csv(data, file_name):
    """Saves the dataset to a CSV file."""
    with open(file_name, "w") as file:
        # Write the header
        file.write("Warehouse_ID,Priority_Level,Package_Count\n")
        # Write each row
        for row in data:
            file.write(",".join(map(str, row)) + "\n")


######### YOUR CODE GOES HERE ---  You shoud define here two_level_sorting and the 3 sorting functions

### Your three sorting functions should have global variable named as counter. So do not return it.
# Bubble Sort implementation to sort a list of lists based on a specific key (index)
def bubble_sort(array, key_index):
    global counter
    # Make a copy of the input array to avoid modifying the original list
    array = array.copy()
    n = len(array)
    # Outer loop to iterate over the array
    for i in range(n):
        # Inner loop to compare adjacent elements
        for j in range(0, n - i - 1):
            counter += 1  # Increment the comparison counter
            # Swap elements if they are in the wrong order
            if array[j][key_index] > array[j + 1][key_index]:
                array[j], array[j + 1] = array[j + 1], array[j]
    # Return the sorted array
    return array

# Merge Sort implementation to sort a list of lists based on a specific key (index)
def merge_sort(array, index):
    # Helper function to merge two sorted lists
    def merge(left, right, index):
        global counter
        result = []
        i = j = 0
        # Merge the two lists by comparing their elements
        while i < len(left) and j < len(right):
            if left[i][index] <= right[j][index]:
                result.append(left[i])  # Append the smaller element
                i += 1
            else:
                counter += 1  # Increment the comparison counter
                result.append(right[j])  # Append the smaller element
                j += 1

        # Add remaining elements from the left list
        while i < len(left):
            result.append(left[i])
            i += 1

        # Add remaining elements from the right list
        while j < len(right):
            result.append(right[j])
            j += 1

        # Return the merged list
        return result

    # Base case: If the list has less than 2 elements, it is already sorted
    if len(array) < 2:
        return array[:]

    # Split the array into two halves and sort each half recursively
    mid = len(array) // 2
    left = merge_sort(array[:mid], index)
    right = merge_sort(array[mid:], index)

    # Merge the two sorted halves
    return merge(left, right, index)

# Quick Sort implementation to sort a list of lists based on a specific key (index)
def quick_sort(array, index):
    global counter
    # Base case: If the list has 1 or no elements, it is already sorted
    if len(array) <= 1:
        return array

    counter += 1  # Increment the recursion counter
    # Choose the middle element as the pivot
    n = len(array) // 2
    pivot = array[n][index]

    # Initialize lists for elements smaller, larger, and equal to the pivot
    smaller_than_pivot = []
    larger_than_pivot = []
    pivots = []

    # Partition the array based on the pivot value
    for element in array:
        if element[index] < pivot:
            smaller_than_pivot.append(element)
        elif element[index] > pivot:
            larger_than_pivot.append(element)
        else:
            pivots.append(element)

    # Recursively sort the smaller and larger partitions
    smaller_sorted = quick_sort(smaller_than_pivot, index)
    larger_sorted = quick_sort(larger_than_pivot, index)

    # Return the concatenated result of smaller, pivot, and larger lists
    return smaller_sorted + pivots + larger_sorted

# Two-level sorting function that sorts based on priority level and package count
def two_level_sorting(sorting_func, array):
    global counter

    # Handle the edge case where there is only one element
    if len(array) == 1:
        print('There is 1 element in the input')
        return array, 0, 0

    # First-level sorting based on priority level (column index 1)
    counter = 0
    sorted_by_pl = sorting_func(array, 1)
    pl_iterations = counter  # Store the number of iterations for the first level

    # Reset the counter for the second-level sorting
    counter = 0

    # Group rows by their priority level
    groups = {}
    for row in sorted_by_pl:
        priority_level = row[1]
        if priority_level not in groups:
            groups[priority_level] = []
        groups[priority_level].append(row)

    # Perform second-level sorting within each priority group based on package count
    final_sorted_array = []
    for priority_level in groups.keys():
        group = groups[priority_level]
        if len(group) > 1:
            sorted_group = sorting_func(group, 2)
            final_sorted_array.extend(sorted_group)
        else:
            final_sorted_array.extend(group)

    pc_iterations = counter  # Store the number of iterations for the second level

    # Return the final sorted array and iteration counts
    return final_sorted_array, pl_iterations, pc_iterations

#########

def write_output_file(
        bubble_sorted, merge_sorted, quick_sorted,
        bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
        bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
        merge_check, quick_check
):
    """Write sorted results and comparisons to the output file."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write("=== Bubble Sorted Results ===\n")
        # file.write(bubble_sorted.to_string() + "\n\n")
        file.write("Warehouse_ID  Priority_Level  Package_Count\n")
        file.write("-" * 40 + "\n")
        for row in bubble_sorted:
            file.write(f"{row[0]:<12}  {row[1]:<14}  {row[2]:<13}\n")
        file.write("\n")
        file.write("=== Comparison Results ===\n")
        if merge_check:
            file.write("Merge and Bubble sorts are identical.\n")
        else:
            file.write("Merge and Bubble sorts differ.\n")

        if quick_check:
            file.write("Quick and Bubble sorts are identical.\n")
        else:
            file.write("Quick and Bubble sorts differ.\n")

        file.write("\n=== Sort Performance Metrics ===\n")
        file.write(f"Bubble priority sort iteration count: {bubble_sort_pl_iterations}\n")
        file.write(f"Merge priority sort n_of right array is smaller than left: {merge_sort_pl_counter}\n")
        file.write(f"Quick priority sort recursive step count: {quick_sort_pl_counter}\n\n")

        file.write(f"Bubble package count sort iteration count: {bubble_sort_pc_iterations}\n")
        file.write(f"Merge package count n_of right array is smaller than left: {merge_sort_pc_counter}\n")
        file.write(f"Quick package count sort recursive step count: {quick_sort_pc_counter}\n")

    print(f"Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    # File paths and dataset size
    # Specify paths for input and output files
    INPUT_FILE = "hw05_input.csv"  # Path where the generated dataset will be saved
    OUTPUT_FILE = "hw05_output.txt"  # Path where the sorted results and metrics will be saved
    SIZE = 100  # Number of warehouses in the dataset

    # Generate the dataset
    dataset = generate_logistics_dataset(SIZE,
                                         max_packages=100)  # Generate a dataset with SIZE warehouses and max_packages packages

    # Save the generated dataset to the input file
    save_to_csv(dataset, INPUT_FILE)

    ###############################################################################################################
    # Perform sorting and counting operations
    # Sort using Bubble Sort and count iterations for Priority Level (_pl_) and Package Count (_pc_)
    bubble_sorted, bubble_sort_pl_iterations, bubble_sort_pc_iterations = two_level_sorting(bubble_sort, dataset)

    # Sort using Merge Sort and count recursive steps for Priority Level and Package Count
    merge_sorted, merge_sort_pl_counter, merge_sort_pc_counter = two_level_sorting(merge_sort, dataset)

    # Sort using Quick Sort and count recursive steps for Priority Level and Package Count
    quick_sorted, quick_sort_pl_counter, quick_sort_pc_counter = two_level_sorting(quick_sort, dataset)
    ###############################################################################################################

    # Comparisons
    # Check if Merge Sort results match Bubble Sort results
    merge_check = merge_sorted == bubble_sorted

    # Check if Quick Sort results match Bubble Sort results
    quick_check = quick_sorted == bubble_sorted

    # Write results and metrics to the output file
    write_output_file(
        bubble_sorted, merge_sorted, quick_sorted,
        bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
        bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
        merge_check, quick_check
    )



