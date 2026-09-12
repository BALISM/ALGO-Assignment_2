# ------------------------------------------------------------------ #
#  sorters.py                                                          #
#  Three classic O(n^2) sorting algorithms, each implemented from     #
#  scratch and compatible with both numeric and string data.           #
# ------------------------------------------------------------------ #


def bubble_sort(arr):
    """
    Bubble Sort — iterative, comparison-based.

    Passes repeatedly over the list; whenever two neighbours are out of
    order it swaps them.  An early-exit flag lets the algorithm stop as
    soon as a full pass produces no swaps.

    Complexity:
        Best case    O(n)   — input already sorted; exits after one pass
        Average case O(n²)
        Worst case   O(n²)  — input in reverse order
    Stable: Yes  (equal elements keep their original relative order)
    """
    data = list(arr)           # work on a copy; caller's list is unchanged
    length = len(data)
    for pass_num in range(length):
        made_swap = False
        limit = length - pass_num - 1
        for idx in range(limit):
            if data[idx] > data[idx + 1]:
                data[idx], data[idx + 1] = data[idx + 1], data[idx]
                made_swap = True
        if not made_swap:      # already sorted — no need to continue
            break
    return data


def selection_sort(arr):
    """
    Selection Sort — in-place, comparison-based.

    On each iteration, scans the unsorted suffix to find its minimum
    value, then moves that minimum to the front of the suffix.

    Complexity:
        Best case    O(n²)  — must scan entire remaining portion each time
        Average case O(n²)
        Worst case   O(n²)
    Stable: No  (a swap can push an equal element past another)
    """
    data = list(arr)
    length = len(data)
    for boundary in range(length):
        smallest = boundary
        for candidate in range(boundary + 1, length):
            if data[candidate] < data[smallest]:
                smallest = candidate
        if smallest != boundary:
            data[boundary], data[smallest] = data[smallest], data[boundary]
    return data


def insertion_sort(arr):
    """
    Insertion Sort — in-place, adaptive, comparison-based.

    Grows a sorted prefix one element at a time.  Each new element is
    shifted leftward until it sits in the correct position among the
    already-sorted elements.

    Complexity:
        Best case    O(n)   — input already sorted; zero shifts needed
        Average case O(n²)
        Worst case   O(n²)  — input in reverse order; maximum shifts
    Stable: Yes  (shifts only elements that are *strictly* greater)
    """
    data = list(arr)
    for pos in range(1, len(data)):
        current = data[pos]
        cursor = pos - 1
        while cursor >= 0 and data[cursor] > current:
            data[cursor + 1] = data[cursor]
            cursor -= 1
        data[cursor + 1] = current
    return data


# ------------------------------------------------------------------ #
#  Self-test: run this file directly to verify correctness             #
# ------------------------------------------------------------------ #
if __name__ == '__main__':
    numeric_sample = [5, 2, 9, 1, 5, 6, -3, 0]
    string_sample  = ['DL', 'AA', 'UA', 'AA', 'WN', 'B6']

    for label, func in [
        ('bubble_sort',    bubble_sort),
        ('selection_sort', selection_sort),
        ('insertion_sort', insertion_sort),
    ]:
        result_nums = func(numeric_sample)
        result_strs = func(string_sample)
        assert result_nums == sorted(numeric_sample), f'{label} failed on numerics'
        assert result_strs == sorted(string_sample),  f'{label} failed on strings'
        print(f'{label}: PASS  nums={result_nums}  strs={result_strs}')
