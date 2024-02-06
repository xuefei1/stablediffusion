
"""
QuickSort, worst time O(n^2), average (nlogn), in place, not stable

first picking a pivot, then all the elements less than the pivot go in front of the pivot,
all elements greater/equal than the pivot go after the pivot, then break the resulting array at pivot, recursively
call partition on each sub array
pick the pivot, then have two pointers at the front and end of the array, while front pointer element is less than pivot continue
moving right, while end pointer element is greater than pivot continue moving left, if both stopped, swap the element and continue

QuickSort partition:
Step 1 - Choose the highest index value has pivot
Step 2 - Take two variables to point left and right of the list excluding pivot
Step 3 - left points to the low index
Step 4 - right points to the high
Step 5 - while value at left is less than pivot move right
Step 6 - while value at right is greater than pivot move left
Step 7 - if both step 5 and step 6 does not match swap left and right
Step 8 - if left >= right, the point where they met, swap with pivot

QuickSort algorithm:
Step 1 - Make the right-most index value pivot
Step 2 - partition the array using pivot value
Step 3 - quick_sort left partition recursively
Step 4 - quick_sort right partition recursively, do not include swapped pivot index
"""
def quick_sort(arr, left, right):
    if left >= right: return
    pivot_idx = partition_v2(arr, left, right)
    quick_sort(arr, left, pivot_idx - 1)
    quick_sort(arr, pivot_idx + 1, right)

def partition(arr, left, right):
    pivot_idx = left # it is essential to remember this pivot index
    pivot = arr[pivot_idx]
    while left < right:
        while left < len(arr) and arr[left] <= pivot:
            left += 1
        while arr[right] > pivot:
            right -= 1
        if left >= right:
            break
        arr[left], arr[right] = arr[right], arr[left]
    arr[right], arr[pivot_idx] = arr[pivot_idx], arr[right]
    return right


def partition_v2(arr, lo, hi):
    """
    Logically, this is equivalent to populating L and G subsets from the remaining U set.
    """
    pivot = arr[lo]
    mi = lo
    for k in range(lo + 1, hi + 1):
        if arr[k] < pivot:
            mi += 1
            arr[mi], arr[k] = arr[k], arr[mi]
    arr[lo], arr[mi] = arr[mi], arr[lo]
    return mi


if __name__ == "__main__":
    array = [1,4,6,2,3,7,9,3,-2,-5,-5,3,2,6,8,4,11]
    quick_sort(array, 0, len(array) - 1)
    print(array)
