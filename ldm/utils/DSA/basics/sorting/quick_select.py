from basics.sorting.quick_sort import partition_v2

def quick_select(arr, k):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        pivot_idx = partition_v2(arr, lo, hi)
        if pivot_idx >= k:
            hi = pivot_idx - 1
        if pivot_idx <= k:
            lo = pivot_idx + 1
    return arr[k]


if __name__ == "__main__":
    # array = [1,4,6,2,3,7,9,3,-2,-5,-5,3,2,6,8,4,11]
    # print(quick_select(array, 3))

    import random
    vals = list(range(10000))
    n = 0
    for _ in range(100000):
        inds = random.sample(vals, k=3)
        inds.sort()
        idx = inds[1]
        v1, v2 = vals[:idx], vals[idx + 1:]
        if len(v1) == 0 or len(v2) == 0:
            n += 1
        elif len(v1) / len(v2) > 9 or len(v1) / len(v2) < (1/9):
            n += 1
    print(n / 100000)
