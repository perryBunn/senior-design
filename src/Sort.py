from lib import Item


MIN_MERGE = 32


def item_sort(unsorted: [Item]) -> list:
    """
    Will sort the items in order from largest to smallest

    :param unsorted: list of unsorted items
    :return: sorted list of items
    """
    raise NotImplementedError


def calc_min_run(n) -> int:
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n+r


def insertion(arr, left, right) -> list:
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1
    return arr


def merge(array, left_index, right_index):
    if left_index >= right_index:
        return

    middle = (left_index + right_index)//2
    merge(array, left_index, middle)
    merge(array, middle + 1, right_index)
    __combine(array, left_index, right_index, middle)


def __combine(arr, left, right, mid):
    left_copy = arr[left:mid + 1]
    right_copy = arr[mid + 1:right + 1]

    left_index = 0
    right_index = 0
    sorted_index = left
    while left_index < len(left_copy) and right_index < len(right_copy):
        if left_copy[left_index] <= right_copy[right_index]:
            arr[sorted_index] = left_copy[left_index]
            left_index = left_index + 1
        else:
            arr[sorted_index] = right_copy[right_index]
            right_index = right_index + 1
        sorted_index = sorted_index + 1
    while left_index < len(left_copy):
        arr[sorted_index] = left_copy[left_index]
        left_index = left_index + 1
        sorted_index = sorted_index + 1
    while right_index < len(right_copy):
        arr[sorted_index] = right_copy[right_index]
        right_index = right_index + 1
        sorted_index = sorted_index + 1
    return arr


def tim_sort(arr: list) -> list:
    n = len(arr)
    min_run = calc_min_run(n)

    for start in range(0, n, min_run):
        end = min(start+min_run-1, n-1)
        insertion(arr, start, end)

    size = min_run
    while size < n:
        for left in range(0, n, 2*size):
            right = min(left+2*size-1, n-1)

            merge(arr, left, right)

        size = 2*size
    return arr
