# ================================================================== #
#  sorters.py                                                          #
#  Bubble, Selection, and Insertion sort — hand-coded from scratch.    #
#  All three accept lists of numbers or strings interchangeably.       #
# ================================================================== #


# ------------------------------------------------------------------ #
#  Bubble Sort                                                         #
# ------------------------------------------------------------------ #
def bubble_sort(arr):
    """
    Bubble Sort.

    Strategy: walk through the list repeatedly, pushing large values
    rightward one position at a time via adjacent swaps.  Stops early
    when a complete pass has zero swaps (list already sorted).

    Time complexity
    ---------------
    Best    : O(n)    each element already in place → one clean pass
    Average : O(n²)
    Worst   : O(n²)   fully reversed input

    Stable  : Yes — two equal elements are never swapped past each other.
    """
    working = list(arr)
    unsorted_end = len(working) - 1

    while unsorted_end > 0:
        last_swap = 0                       # track where the last swap happened
        for i in range(unsorted_end):
            if working[i] > working[i + 1]:
                working[i], working[i + 1] = working[i + 1], working[i]
                last_swap = i
        unsorted_end = last_swap            # everything after last_swap is sorted
    return working


# ------------------------------------------------------------------ #
#  Selection Sort                                                      #
# ------------------------------------------------------------------ #
def selection_sort(arr):
    """
    Selection Sort.

    Strategy: treat the list as a sorted prefix (initially empty) and
    an unsorted suffix (initially the whole list).  Each pass locates
    the smallest item in the suffix and appends it to the prefix.

    Time complexity
    ---------------
    Best    : O(n²)   full suffix scan is always required
    Average : O(n²)
    Worst   : O(n²)

    Stable  : No — the swap may leapfrog an equal element.
    """
    working = list(arr)
    n = len(working)
    prefix_end = 0

    while prefix_end < n:
        # find the index of the minimum value in working[prefix_end:]
        min_pos = prefix_end
        for j in range(prefix_end + 1, n):
            if working[j] < working[min_pos]:
                min_pos = j

        if min_pos != prefix_end:
            working[prefix_end], working[min_pos] = (
                working[min_pos], working[prefix_end]
            )
        prefix_end += 1

    return working


# ------------------------------------------------------------------ #
#  Insertion Sort                                                      #
# ------------------------------------------------------------------ #
def insertion_sort(arr):
    """
    Insertion Sort.

    Strategy: iterate from left to right; for each element, shift it
    leftward through the already-sorted prefix until it reaches the
    correct position (like inserting a playing card into a hand).

    Time complexity
    ---------------
    Best    : O(n)    already sorted → zero shifts per element
    Average : O(n²)
    Worst   : O(n²)   reversed input → maximum shifts per element

    Stable  : Yes — only elements *strictly* greater than the key are
               shifted, so equal elements keep their original order.
    """
    working = list(arr)

    for right in range(1, len(working)):
        key_val  = working[right]
        hole     = right           # position where key_val will land

        while hole > 0 and working[hole - 1] > key_val:
            working[hole] = working[hole - 1]
            hole -= 1

        working[hole] = key_val

    return working


# ================================================================== #
#  Correctness check — run directly to validate both data types        #
# ================================================================== #
def _run_tests():
    test_cases = [
        ([5, 2, 9, 1, 5, 6, -3, 0], 'integers'),
        ([3.14, 1.41, 2.71, 0.57], 'floats'),
        (['DL', 'AA', 'UA', 'AA', 'WN', 'B6'], 'strings'),
    ]
    algorithms = [
        ('bubble_sort',    bubble_sort),
        ('selection_sort', selection_sort),
        ('insertion_sort', insertion_sort),
    ]
    all_passed = True
    for label, fn in algorithms:
        for data, dtype in test_cases:
            got      = fn(data)
            expected = sorted(data)
            ok       = got == expected
            status   = 'PASS' if ok else 'FAIL'
            print(f'  {label:<16}  {dtype:<10}  {status}')
            if not ok:
                print(f'    expected: {expected}')
                print(f'    got:      {got}')
                all_passed = False
    return all_passed


if __name__ == '__main__':
    print('Running correctness tests...\n')
    success = _run_tests()
    print('\nAll tests passed.' if success else '\nSome tests FAILED.')
