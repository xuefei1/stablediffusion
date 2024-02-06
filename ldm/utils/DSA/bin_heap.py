"""
Heapify in this way runs in linear time.
"""


def heapify(arr):
    for i in range((len(arr) - 1) // 2, -1, -1):
        max_heap(arr, i)


def max_heap(arr, i):
    left = 2 * i + 1
    right = 2 * i + 2
    _max = i
    if left < len(arr) and arr[left] > arr[_max]:
        _max = left
    if right < len(arr) and arr[right] > arr[_max]:
        _max = right
    if _max != i:
        arr[i], arr[_max] = arr[_max], arr[i]
        max_heap(arr, _max)
