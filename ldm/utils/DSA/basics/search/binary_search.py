

def binary_search(arr, tgt):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == tgt:
            return mid
        elif arr[mid] < tgt:
            lo = mid + 1
        else:
            hi = mid - 1
    print("Not found, next greater element is at {}".format(lo))
    return -1 # lo will point to the next greater element


"""
Use binary search to find an element in a rotated sorted array

The key is that half of the array is still sorted, we just need to determine if the target is in the sorted range
If yes, chop the other half, else chop this half
"""
def binary_search_rotated_array(rot_arr, tgt):
    lo, hi = 0, len(rot_arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if rot_arr[mid] == tgt:
            return mid
        if rot_arr[lo] <= rot_arr[mid]: # left half is sorted
            # if tgt is indeed in this half
            if rot_arr[lo] <= tgt < rot_arr[mid]:
                hi = mid - 1
            else: # otherwise it could be in the other half
                lo = mid + 1
        else: # right half is sorted
            if rot_arr[mid] < tgt <= rot_arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


"""
Find the point of rotation for a rotated sorted array

The idea is to keep chopping off the sorted part until we find the pivot index
"""
def find_rot_idx(rot_arr):
    lo, hi = 0, len(rot_arr) - 1
    while rot_arr[lo] > rot_arr[hi]: # when this condition is no longer satisfied, we no longer have a sorted array
        mid = lo + (hi - lo) // 2
        if rot_arr[mid] > rot_arr[hi]:
            # mid > end element meaning the rotate index is in the right sub array, chop off left
            lo = mid + 1
        else:
            # otherwise mid element< right element and pivot index is in the left sub array
    		# here we don't do right = mid - 1 to handle the case 15 1 2 3... and mid element= 1
            hi = mid
    # when arr[lo] is no longer greater than arr[hi], we have a sorted array and lo is the start
    return lo


"""
Find if an element exists in a sorted 2D matrix, every row/column is increasing left2right/top2bottom
"""
def find_element(mat, tgt):
    row, col = 0, len(mat[0])-1
    while row < len(mat) and col >= 0:
        if mat[row][col] == tgt:
            return True
        if mat[row][col] < tgt:
            row += 1
        else:
            col -= 1
    return False


"""
See the effect of l < r ; r = m and l <= r ; r = m - 1
"""
def bs1(arr, target):
    """
    If using l < r and r = m, make sure initial r is len(arr).
    """
    visited_m_vals = []
    l, r, m = 0, len(arr), None
    while l < r:
        m = (r - l) // 2 + l
        visited_m_vals.append(m)
        if arr[m] == target:
            print(f"BS1 found, l={l}, r={r}, m={m}, visited_m_vals={visited_m_vals}")
            return m
        elif arr[m] < target:
            l = m + 1
        else:
            r = m
    print(f"BS1 cannot find, l={l}, r={r}, m={m}, visited_m_vals={visited_m_vals}")
    return -1


def bs2(arr, target):
    """
    If using l <= r and r = m-1, make sure initial r is len(arr)-1.
    """
    visited_m_vals = []
    l, r, m = 0, len(arr) - 1, None
    while l <= r:
        m = (r - l) // 2 + l
        visited_m_vals.append(m)
        if arr[m] == target:
            print(f"BS2 found, l={l}, r={r}, m={m}, visited_m_vals={visited_m_vals}")
            return m
        elif arr[m] < target:
            l = m + 1
        else:
            r = m - 1
    print(f"BS2 cannot find, l={l}, r={r}, m={m}, visited_m_vals={visited_m_vals}")
    return -1


def bs3(arr, target):
    """
    No == comparison during search.
    """
    visited_m_vals = []
    l, r, m = 0, len(arr), None
    while l < r:
        m = (r - l) // 2 + l
        visited_m_vals.append(m)
        if arr[m] < target:
            l = m + 1
        else:
            r = m
    if arr[m] == target:
        print(f"BS3 found, l={l}, r={r}, m={m}, visited_m_vals={visited_m_vals}")
    else:
        print(f"BS3 cannot find, l={l}, r={r}, m={m}, visited_m_vals={visited_m_vals}")
    return m


def bs4(arr, target):
    """
    No == comparison during search.
    """
    visited_m_vals = []
    l, r, m = 0, len(arr)-1, None
    while l <= r:
        m = (r - l) // 2 + l
        visited_m_vals.append(m)
        if arr[m] < target:
            l = m + 1
        else:
            r = m - 1
    if arr[m] == target:
        print(f"BS4 found, l={l}, r={r}, m={m}, visited_m_vals={visited_m_vals}")
    else:
        print(f"BS4 cannot find, l={l}, r={r}, m={m}, visited_m_vals={visited_m_vals}")
    return m


if __name__ == "__main__":
    print("Even length input")
    bs1([1, 2, 3, 5, 6, 7, 8, 9], 11)
    bs2([1, 2, 3, 5, 6, 7, 8, 9], 11)
    bs3([1, 2, 3, 5, 6, 7, 8, 9], 11)
    bs4([1, 2, 3, 5, 6, 7, 8, 9], 11)
    bs1([1, 2, 3, 5, 6, 7, 8, 9], 1)
    bs2([1, 2, 3, 5, 6, 7, 8, 9], 1)
    bs3([1, 2, 3, 5, 6, 7, 8, 9], 1)
    bs4([1, 2, 3, 5, 6, 7, 8, 9], 1)

    print("Odd length input")
    bs1([1, 2, 3, 5, 6, 7, 8, 9, 10], 11)
    bs2([1, 2, 3, 5, 6, 7, 8, 9, 10], 11)
    bs3([1, 2, 3, 5, 6, 7, 8, 9, 10], 11)
    bs4([1, 2, 3, 5, 6, 7, 8, 9, 10], 11)
    bs1([1, 2, 3, 5, 6, 7, 8, 9, 10], 1)
    bs2([1, 2, 3, 5, 6, 7, 8, 9, 10], 1)
    bs3([1, 2, 3, 5, 6, 7, 8, 9, 10], 1)
    bs4([1, 2, 3, 5, 6, 7, 8, 9, 10], 1)
