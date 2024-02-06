import math
import collections


def num_subarray_sum_k(nums, k):
    """
    Subarray Sum Equals K
    Given an array of integers and an integer k, you need to find the total number of continuous subarrays whose sum equals to k.
    nums could contain negative numbers, so sliding window won't be beneficial

    O(n) time, O(n) space solution:
    Use a dict to track the cumulative sum at each index and the number of times that sum is encountered
    If a later index gives a sum difference of k, we would know how many times it occurred
    """
    sums = {0:1} # empty array gives a sum of 0
    cum_sum = 0
    count = 0
    for i, num in enumerate(nums):
        cum_sum += num

        # Must check first and then update, in case k = 0
        if cum_sum - k in sums:
            count += sums[cum_sum - k]

        if cum_sum not in sums:
            sums[cum_sum] = 0
        sums[cum_sum] += 1

    return count


def num_triplet_sum(nums):
    """
    Count the triplets
    Given an array of distinct integers. The task is to count all the triplets such that sum of two elements equals the third element.

    O(n^2) time O(log(n)) space solution:
    Because we can re-order the array, sort first
    For each number in the array, check if any two number adds to it in the sorted array using left and right pointers
    If sum is less than target, increase left, else decrease right
    """
    nums = nums.sort(reverse=False)
    rv = 0
    for i in range(len(nums)-1, 1, -1):
        target = nums[i]
        left, right = 0, len(nums) - 1
        while left < right:
            if nums[left] + nums[right] == target:
                rv += 1
                left += 1

            elif nums[left] + nums[right] < target:
                left += 1
            else:
                right -= 1
    return rv


def max_subarray_sum(nums):
    """
    Maximum Subarray
    Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

    O(n) time, O(1) space solution:
    Kadane's algorithm
    If we know the maximum subarray sum ending at position i, what is the maximum subarray sum ending at position i + 1?
    The answer: maximun subarray sum ending at position i + 1 includes the maximum subarray sum ending at position i as a prefix
                or
                position i + 1
    Thus, compute the maximum subarray sum ending at position i by iterating over the array.
    """
    curr = 0
    rv = 0
    for num in nums:
        curr += num
        if curr < num:
            curr = num
        rv = max(curr, rv)
    return rv


def rearrange(arr):
    """
    Given a sorted array of positive integers.
    Rearrange the array elements alternatively i.e first element should be max value, second should be min value, third should be second max, fourth should be second min and so on...

    How does expression “arr[i] += arr[max_index] % max_element * max_element” work ?
    The purpose of this expression is to store two elements at index arr[i].
    arr[max_index] is stored as multiplier and “arr[i]” is stored as remainder.
    For example in {1 2 3 4 5 6 7 8 9}, max_element is 10 and we store 91 at index 0. With 91, we can get original element as 91%10 and new element as 91/10.
    """
    # Initialize index of first minimum
    # and first maximum element
    n = len(arr)
    max_idx = n - 1
    min_idx = 0

    # Store maximum element of array + 1
    max_elem = arr[n - 1] + 1

    # Traverse array elements
    for i in range(0, n):

        # At even index : we have to put maximum element
        if i % 2 == 0:
            arr[i] += (arr[max_idx] % max_elem) * max_elem
            max_idx -= 1

        # At odd index : we have to put minimum element
        else:
            arr[i] += (arr[min_idx] % max_elem) * max_elem
            min_idx += 1

    # array elements back to it's original form
    for i in range(0, n):
        arr[i] = arr[i] // max_elem


def n_inversions_in_array(arr):
    """
    Count the number of inversions in an array
    Inversion Count for an array indicates – how far (or close) the array is from being sorted.
    If array is already sorted then inversion count is 0. If array is sorted in reverse order that inversion count is the maximum.
    Formally speaking, two elements a[i] and a[j] form an inversion if a[i] > a[j] and i < j

    The number of inversion is the sum of the number of elements less than a element that are to the right of it.
    Modified merge sort: count the inversions during merge
    """
    _, count = n_inversions_merge_sort(arr)
    return count

def n_inversions_merge_sort(arr):
    if len(arr) <= 1: return arr, 0
    mid = len(arr) // 2
    left_subarr, l_rv = n_inversions_merge_sort(arr[:mid])
    right_subarr, r_rv = n_inversions_merge_sort(arr[mid:])
    rv_arr, n_inversions = n_inversions_merge(left_subarr, right_subarr)
    return rv_arr, n_inversions + l_rv + r_rv

def n_inversions_merge(l_arr, r_arr):
    i, j = 0, 0
    rv_arr = []
    count = 0
    while i < len(l_arr) and j < len(r_arr):
        if l_arr[i] < r_arr[j]:
            rv_arr.append(l_arr[i])
            i += 1
        else:
            rv_arr.append(r_arr[j])
            count += len(l_arr) - i
            j += 1
    while i < len(l_arr):
        rv_arr.append(l_arr[i])
        i += 1
    while j < len(r_arr):
        rv_arr.append(r_arr[j])
        j += 1
    return rv_arr, count


def majorityElement(nums):
    """
    Majority Element II
    Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.
    Note: The algorithm should run in linear time and in O(1) space.

    Input: [1,1,1,3,3,2,2,2]
    Output: [1,2]

    At most two answers
    Modified Moore's voting: keep track of two majority candidates
    """
    cand_1, cand_2 = None, None
    n_supports_1, n_supports_2 = 0, 0
    for n in nums:
        if n == cand_1:
            n_supports_1 += 1
        if n == cand_2:
            n_supports_2 += 1
        if n != cand_1 and n != cand_2:
            if n_supports_1 == 0:
                if n != cand_2: # track each candidate separately, this way, cand_1 != cand_2
                    cand_1 = n
                    n_supports_1 += 1
            elif n_supports_2 == 0:
                if n != cand_1: # track each candidate separately, this way, cand_1 != cand_2
                    cand_2 = n
                    n_supports_2 += 1
            else:
                n_supports_1 -= 1
                n_supports_2 -= 1
    # print("cand_1: {}, cand_2:{}".format(cand_1, cand_2))
    # Count the number of occurrences
    n_supports_1, n_supports_2 = 0, 0
    for n in nums:
        if n == cand_1: n_supports_1 += 1
        if n == cand_2: n_supports_2 += 1
    # Make sure appears over 1/3 times
    rv = []
    if n_supports_1 > len(nums) / 3: rv.append(cand_1)
    if n_supports_2 > len(nums) / 3: rv.append(cand_2)
    return rv


def sort_array_0_1_2(arr):
    """
    Sort an array of 0s, 1s and 2s
    a.k.a Dutch national flag problem
    Given an array A of size N containing 0s, 1s, and 2s; you need to sort the array in ascending order.

    O(n) time O(1) space solution:
    Three pointers: i keep the next index to put a 0, j keep the next index to put a 2, curr keep the current comparison index
    compare each number with 1: if less, swap value at i and curr, increment both
    if more, swap value at j and curr, decrement j
    if equal, increment curr
    """
    i, j, curr = 0, len(arr)-1, 0
    while curr <= j:
        if arr[curr] < 1:
            arr[i], arr[curr] = arr[curr], arr[i]
            curr += 1
            i += 1
        elif arr[curr] > 1:
            arr[j], arr[curr] = arr[curr], arr[j]
            j -= 1
        else:
            curr += 1
    return arr


def equilibrium_point(arr):
    """
    Equilibrium point
    Given an array A of N positive numbers. The task is to find a position where equilibrium first occurs in the array.
    Equilibrium position in an array is a position such that the sum of elements before it is equal to the sum of elements after it.

    O(n) time, O(1) space solution:
    compute total sum, maintain running left sum, right sum then = total - left - curr num
    """
    total_sum = sum(arr)
    left_running_sum = 0
    for i, num in enumerate(arr):
        if total_sum - left_running_sum - num == left_running_sum:
            return i
        left_running_sum += num
    return -1


def sort_arr_with_ref_inds(arr, inds):
    """
    We need to sort array A, array B contains indices to corresponding elements in array A with their correct sorted location
    (at cost of O(n) with constant space)

    at index i, swap arr[i] and inds[i] to the right position if it's not there yet
    """
    curr_idx = 0
    while curr_idx < len(arr):
        tgt_idx = inds[curr_idx] - 1
        if curr_idx != tgt_idx:
            arr[curr_idx], arr[tgt_idx] = arr[tgt_idx], arr[curr_idx]
            inds[curr_idx], inds[tgt_idx] = inds[tgt_idx], inds[curr_idx]
        else:
            curr_idx += 1
    return arr


def maxRotateFunction(A) -> int:
    """
    Given an array of integers A and let n to be its length.

    Assume Bk to be an array obtained by rotating the array A k positions clock-wise, we define a "rotation function" F on A as follow:

    F(k) = 0 * Bk[0] + 1 * Bk[1] + ... + (n-1) * Bk[n-1].

    Calculate the maximum value of F(0), F(1), ..., F(n-1).

    Example:
        A = [4, 3, 2, 6]
        F(0) = (0 * 4) + (1 * 3) + (2 * 2) + (3 * 6) = 0 + 3 + 4 + 18 = 25
        F(1) = (0 * 6) + (1 * 4) + (2 * 3) + (3 * 2) = 0 + 4 + 6 + 6 = 16
        F(2) = (0 * 2) + (1 * 6) + (2 * 4) + (3 * 3) = 0 + 6 + 8 + 9 = 23
        F(3) = (0 * 3) + (1 * 2) + (2 * 6) + (3 * 4) = 0 + 2 + 12 + 12 = 26
        So the maximum value of F(0), F(1), F(2), F(3) is F(3) = 26.
    """
    arr_sum = sum(A)  # equivalent to increment multiplier for each array value
    F_0 = rv = sum([i * v for i, v in enumerate(A)])
    F_prev = F_0
    n = len(A)
    for i in range(1, n):
        # First increment multipliers for all values
        # Last value in the current rotation should be multiplied with zero, i.e. minus its prev value, which is (n-1) * last value in rotated array
        # We also incremented its multiplier, i.e. minus it one more time
        F_n = F_prev + arr_sum - (n - 1) * A[n - i] - A[n - i]
        rv = max(rv, F_n)
        F_prev = F_n
    return rv


def findMedianSortedArrays(nums1, nums2) -> float:
    if len(nums1) == 0 or len(nums2) == 0:
        rv_nums = nums1 if len(nums1) > 0 else nums2
        return rv_nums[len(rv_nums) // 2] if len(rv_nums) % 2 != 0 else (rv_nums[len(rv_nums) // 2] + rv_nums[len(rv_nums) // 2 - 1]) / 2
    if len(nums1) > len(nums2):
        return findMedianSortedArrays(nums2, nums1)

    start, end = 0, len(nums1)
    while start <= end:
        mid1 = start + (end - start) // 2
        mid2 = math.ceil((len(nums1) + len(nums2)) / 2) - mid1
        # mid2 = lower_len - mid1

        l_cand_1 = nums1[mid1 - 1] if mid1 > 0 else float("-inf")
        r_cand_1 = nums1[mid1] if mid1 < len(nums1) else float("inf")

        l_cand_2 = nums2[mid2 - 1] if mid2 > 0  else float("-inf")
        r_cand_2 = nums2[mid2] if mid2< len(nums2) else float("inf")

        if l_cand_1 <= r_cand_2 and l_cand_2 <= r_cand_1:
            # compute median
            if (len(nums1) + len(nums2)) % 2 != 0:
                return max(l_cand_1, l_cand_2)
            else:
                return (max(l_cand_1, l_cand_2) + min(r_cand_1, r_cand_2)) / 2
        elif l_cand_1 > r_cand_2:
            # move left
            end = mid1 - 1
        else:
            # move right
            start = mid1 + 1
    assert False


class Solution1131:
    """
    Given two arrays of integers with equal lengths, return the maximum value of:
    |arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|
    where the maximum is taken over all 0 <= i, j < arr1.length.

    The goal is to maximize the Manhattan distance between pairs of 3D points (arr1[i], arr2[i], i)
    Transforms Manhattan distance to Chebyshev distance:
    ++, +-, -+, --
    Then find the max along one dimension
    since |arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j| equals
    the max of
    [
                arr1[i]+arr2[i]+i - (arr1[j]+arr2[j]+j),
                arr1[i]-arr2[i]+i - (arr1[j]-arr2[j]+j),
                arr1[i]+arr2[i]-i - (arr1[j]+arr2[j]-j),
                arr1[i]-arr2[i]-i - (arr1[j]-arr2[j]-j),
    ]
    """
    def maxAbsValExpr(self, arr1, arr2) -> int:
        points = []
        for i in range(len(arr1)):
            points.append((
                arr1[i]+arr2[i]+i,
                arr1[i]-arr2[i]+i,
                arr1[i]+arr2[i]-i,
                arr1[i]-arr2[i]-i,
                # -arr1[i]+arr2[i]+i,
                # -arr1[i]-arr2[i]+i,
                # -arr1[i]+arr2[i]-i,
                # -arr1[i]-arr2[i]-i,
            ))
        p = zip(*points)
        rv= 0
        for ps in p:
            rv = max(rv, max(ps)-min(ps))
        return rv


class Solution1124:
    """
    Longest Well-Performing Interval
    We are given hours, a list of the number of hours worked per day for a given employee.
    A day is considered to be a tiring day if and only if the number of hours worked is (strictly) greater than 8.
    A well-performing interval is an interval of days for which the number of tiring days is strictly larger than the number of non-tiring days.
    Return the length of the longest well-performing interval.

    O(N) solution
    finding the longest sub-array with positive sum
    compute running sum at index j, then find the left-most index i where its running sum is 1 less
    1 less ensures that only 1 more tiring days than non-tiring, i.e., longest possible interval
    use a dict for this allows O(1) lookup time
    Example:
    input  =        [6 ,  5,  9,  6,  9,  9,  2]
    running_sums = [-1, -2, -1, -2, -1,  0, -2]
    """
    def longestWPI(self, hours) -> int:
        prefix_sum2idx = {}
        running_sum = 0
        ans = 0
        for end, h in enumerate(hours):
            running_sum += 1 if h > 8 else -1

            # if running sum is positive, we have more tiring days than non-tiring, simply increase the length
            if running_sum > 0:
                ans = max(ans, end + 1)
            elif running_sum - 1 in prefix_sum2idx:
                # running_sum - 1 will give the interval with a positive total sum
                # because sum of interval i to j = prefix_sum[j] - pefix_sum[i]
                # this must be to satisfy the condition, and 1 is the lowest possible positive value here
                # it means there is exactly one more tiring days than non-tiring days
                # we do not consider 2,3,4... because those value indicate that more tiring days, which do not give the longest interval
                # we want the longest interval so we only care about the first (left-most) occurrence of running_sum - 1
                # we check if running_sum - 1 is in the dictionary, i.e., whether we encountered it before
                # if yes, update the max length, store the current running sum for future usage
                # the max length is computed as end - prefix_sum2idx[running_sum - 1],
                # if idx of prefix_sum2idx[running_sum - 1] = 1, and end = 5, the interval is actually 5-1=4, i.e., elements at index [2,3,4,5], so it does not include the element at prefix_sum2idx[running_sum - 1]
                ans = max(ans, end - prefix_sum2idx[running_sum - 1])

            # if running_sum already encountered, do nothing, because we are interested in only the first (left-most) occurrence
            if running_sum not in prefix_sum2idx:
                prefix_sum2idx[running_sum] = end

        return ans


class Solution775:
    """
    We have some permutation A of [0, 1, ..., N - 1], where N is the length of A.
    The number of (global) inversions is the number of i < j with 0 <= i < j < N and A[i] > A[j].
    The number of local inversions is the number of i with 0 <= i < N and A[i] > A[i+1].
    Return true if and only if the number of global inversions is equal to the number of local inversions.

    O(N) solution
    A local inversion is also a global inversion
    We just need to check if there is a global inversion that is not a local inversion
    Maintain the current largest element excluding the current element, we have seen so far, check if it is greater than the next (i+1) element, i.e., non-secutive, global inversion, returns False if yes
    """
    def isIdealPermutation(self, A) -> bool:
        curr_largest = A[0]
        for i in range(1, len(A) - 1):
            if curr_largest > A[i + 1]: return False
            curr_largest = max(curr_largest, A[i])
        return True


class Solution768:
    """
    Max Chunks To Make Sorted II
    Given an array arr of integers (not necessarily distinct), we split the array into some number of "chunks" (partitions), and individually sort each chunk.
    After concatenating them, the result equals the sorted array.
    What is the most number of chunks we could have made?

    O(N) solutions
    Starting from the right, a sub-array can be a chunk only if its min value is >= max value of the remaining left part
    As long as this is satisfied, we will have one more standalone chunk
    We could use left running min + right running max arrays to check this condition
    or use a stack
    The top of the stack represent the current max value, starting from the left
    if we encounter a smaller value than the top of the stack. we must merge this smaller value into the right chunk
    so we keep popping stored max values from the stack, until the top of the stack is smaller than n
    we track the max value along this process, because we could merge multiple existing chunks
    in the end return the stack size
    """
    def maxChunksToSorted(self, arr) -> int:
        min_so_far = []
        max_so_far = []
        for n in arr:
            max_so_far.append(n if len(max_so_far) == 0 else max(max_so_far[-1], n) )
        for i in range(len(arr)-1, -1 ,-1):
            min_so_far.append(arr[i] if len(min_so_far) == 0 else min(min_so_far[-1], arr[i]) )
        min_so_far = min_so_far[::-1]
        ans = 1
        for i in range(len(arr)-1, 0, -1):
            if min_so_far[i] >= max_so_far[i-1]:
                ans += 1
        return ans

    def maxChunksToSortedStack(self, arr) -> int:
        stack = []
        for n in arr:
            curr_chunk_max = n
            while len(stack) > 0 and n < stack[-1]:
                # if the number < max of prev chunk, must merge it into prev chunks
                # for example, if n is the first 1
                # [2,3,4,5,1,1,9]
                # we need to collapse all prev chunks in this case
                # so keep popping from the stack and maintaining the running max of the new chunk
                curr_chunk_max = max(curr_chunk_max, stack.pop())
            # we can add the max of the current chunk
            stack.append(curr_chunk_max)
        return len(stack)


class Solution974:
    """
    Sub-array Sums Divisible by K
    Given an array A of integers, return the number of (contiguous, non-empty) subarrays that have a sum divisible by K.

    O(N) solution using prefix sums
    The sum of any sub-array can be derived from the difference of two prefix sums sum[j]-sum[i], j > i
    if sum[j] and sum[i] have the same remainder after mod K, then sub-array i to j is divisible by K
    sum[j] = K*n + r, sum[i] = K*m + r, sum[j] - sum[i] subtracts out the r
    Therefore, at element i, check how many time we have encountered the remainder sum[i] mod K
    that will be how many more sub-arrays we could find

    If the dividend is negative, I think the remainder could be positive or negative,
    ex. -27%5=-2 or 3, because -27=-6*5+3 and -27=-5*5+(-2).
    But this would cause trouble in our case since we are checking how many times a particular remainder appeared before.
    To transfer the negative remainder to positive, we can add K to it.
    """
    def subarraysDivByK(self, A, K: int) -> int:
        memo = collections.defaultdict(int)
        memo[0] += 1
        ans = 0
        running_sum = 0
        for n in A:
            running_sum += n
            remainder = running_sum % K
            if remainder < 0: remainder += K
            ans += memo[remainder]
            memo[remainder] += 1
        return ans
