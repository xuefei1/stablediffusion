"""
Sliding window is based on the idea of two pointers.
Two pointers is more general than sliding window.
The window can be static or dynamic.
LC 424, 187, 76, 239
"""


def smallest_len_subarray_less_than(arr, k):
    """
    Find the smallest length subarray whose sum is greater than k.
    - When current window sum is less than k, increment right.
    - When current window sum is greater than k, decrement left.
    - Track lowest window length during the process.
    """
    l, r = 0, 0
    s = arr[0]
    ret = float("inf")
    while r < len(arr) - 1 or s > k:
        if arr[r] > k:
            return 1

        if s > k:
            ret = min(ret, r - l + 1)

        if s < k and r < len(arr) - 1:
            r += 1
            s += arr[r]
        else:
            s -= arr[l]
            l += 1

    return ret


if __name__ == "__main__":
    print(smallest_len_subarray_less_than([1,1,2,3,4,8,1,1,9,11,8,3,4,4,5,6,6,12,1,1,1,1,3,4], 25))
