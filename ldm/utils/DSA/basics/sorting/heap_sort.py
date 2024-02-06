
"""
HeapSort O(nlogn) in-place, not stable, Good for constant memory sort
Elements are inserted into the heap, then pop root until heap empty
A heap is a tree like data structure (usually binary) that maintains a certain rule on ordering
A max heap has the largest element at the root, then each parent is always greater than its children
A min heap is the inverse
"""
def heap_sort(arr):
    heapify(arr)
    end = len(arr)
    for i in range(len(arr)-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        end -= 1
        fix_max_heap_violation(arr, 0, end)

def heapify(arr):
    for i in range((len(arr)-1) // 2, -1, -1):
        fix_max_heap_violation(arr, i, len(arr))

def fix_max_heap_violation(arr, i, end_of_unsorted_arr):
    left_chd_idx = 2 * i + 1
    right_chd_idx = 2 * i + 2
    max_idx = i
    if left_chd_idx < end_of_unsorted_arr and arr[left_chd_idx] > arr[max_idx]:
        max_idx = left_chd_idx
    if right_chd_idx < end_of_unsorted_arr and arr[right_chd_idx] > arr[max_idx]:
        max_idx = right_chd_idx
    if max_idx != i:
        arr[max_idx], arr[i] = arr[i], arr[max_idx]
        fix_max_heap_violation(arr, max_idx, end_of_unsorted_arr)

if __name__ == "__main__":
    array = [1,4,6,2,3,7,9,3,-2,-5,-5,3,2,6,8,4,11]
    heap_sort(array)
    print(array)
