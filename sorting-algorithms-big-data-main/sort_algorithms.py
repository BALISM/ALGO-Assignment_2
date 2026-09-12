def bubble_sort(arr):
    """
    Bubble Sort.
    Repeatedly steps through the list, swapping adjacent elements
    if they're in the wrong order, until no swaps are needed.

    Time complexity:
        Best:    O(n)    - already sorted, one pass with no swaps (with early-exit flag)
        Average: O(n^2)
        Worst:   O(n^2)  - reverse sorted input
    Stable: Yes (equal elements never swap past each other)
    """
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def selection_sort(arr):
    """
    Selection Sort.
    Repeatedly finds the minimum element from the unsorted portion
    and swaps it into place at the front.

    Time complexity:
        Best:    O(n^2)  - still scans the whole remaining array every pass
        Average: O(n^2)
        Worst:   O(n^2)
    Stable: No (swapping can move an equal element past another)
    """
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
    return a


def insertion_sort(arr):
    """
    Insertion Sort.
    Builds the sorted array one element at a time, inserting each
    new element into its correct position among the already-sorted
    elements to its left.

    Time complexity:
        Best:    O(n)    - already sorted, each element needs 0 shifts
        Average: O(n^2)
        Worst:   O(n^2)  - reverse sorted input
    Stable: Yes (only shifts elements strictly greater, never swaps equals)
    """
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


if __name__ == '__main__':
    # Quick correctness check on both numeric and string data
    test_nums = [5, 2, 9, 1, 5, 6, -3, 0]
    test_strs = ['DL', 'AA', 'UA', 'AA', 'WN', 'B6']

    for name, fn in [('bubble_sort', bubble_sort),
                      ('selection_sort', selection_sort),
                      ('insertion_sort', insertion_sort)]:
        nums_result = fn(test_nums)
        strs_result = fn(test_strs)
        assert nums_result == sorted(test_nums), f'{name} failed on numbers'
        assert strs_result == sorted(test_strs), f'{name} failed on strings'
        print(f'{name}: OK  nums={nums_result}  strs={strs_result}')