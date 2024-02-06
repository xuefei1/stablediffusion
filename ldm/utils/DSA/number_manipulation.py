
class Solution556:
    """
    Given a positive 32-bit integer n, you need to find the smallest 32-bit integer which has exactly the same digits existing in the integer n and is greater in value than n.
    If no such positive 32-bit integer exists, you need to return -1.
    -Find the first element that is not part of an increasing sequence, starting from the right
    -Swap with the smallest element that's larger than it, considering all digits from its right
    -Sort the remaining digits in the right of it in increasing order
    """
    def nextGreaterElement(self, n: int) -> int:
        digits = [int(c) for c in str(n)]
        i = len(digits)-1
        # find the first element that is not part of an increasing sequence, starting from the right
        while i > 0 and digits[i] <= digits[i-1]:
            i -= 1
        if i == 0: return -1
        i -= 1 # point i to this digit, this is the first swap index
        # find the smallest digit that's larger than it, from the digits to the right of it
        curr_min, swp_idx = float("inf"), -1
        for j in range(len(digits)-1, i, -1):
            if digits[j] > digits[i] and digits[j] < curr_min:
                curr_min = digits[j]
                swp_idx = j
        # swap and sort the digits to the right of it
        digits[i], digits[swp_idx] = digits[swp_idx], digits[i]
        digits = digits[:i+1] + sorted(digits[i+1:])
        ans = int("".join([str(n) for n in digits]))
        return ans if ans < 2**31 - 1 else -1
