import collections


def repeatedSubstringPattern(s: str) -> bool:
    """
    Repeated Substring Pattern
    Given a non-empty string check if it can be constructed by taking a substring of it and appending multiple copies of the substring together.

    Input: "abab"
    Output: True
    Input: "aba"
    Output: False
    """
    double_str = s + s
    double_str = double_str[1:-1]
    return s in double_str


def checkValidPS(s: str) -> bool:
    """
    Valid Parenthesis and Star String
    Given a string containing only three types of characters: '(', ')' and '*', write a function to check whether this string is valid. We define the validity of a string by these rules:

    Any left parenthesis '(' must have a corresponding right parenthesis ')'.
    Any right parenthesis ')' must have a corresponding left parenthesis '('.
    Left parenthesis '(' must go before the corresponding right parenthesis ')'.
    '*' could be treated as a single right parenthesis ')' or a single left parenthesis '(' or an empty string.
    An empty string is also valid.

    Input: "(*))"
    Output: True

    O(n) time O(1) space, 1 pass solution:
    For each *, we could use it as a ( or ) or nothing
    When used as ( the diff increases by 1, when used as ) the diff decreases by 1
    Therefore we track the diff in both cases, we need a maxDiff and a minDiff
    maxDiff should never be negative, when it is, it means we cannot close all ) even if all prev stars are used as (
    minDiff should never go to negative, meaning we shouldn't add ) to a valid string to make it invalid
    In the end, minDiff should be zero
    """
    maxDiff, minDiff = 0, 0
    for c in s:
        maxDiff += 1 if c == "(" or c == "*" else -1
        minDiff += -1 if c == ")" or c == "*" else 1
        if maxDiff < 0: return False
        minDiff = max(minDiff, 0)
    return minDiff == 0


class Solution784:
    """
    Given a string S, we can transform every letter individually to be lowercase or uppercase to create another string.
    Return a list of all possible strings we could create.

    The recur method is not the best, but think about how recur() and recur1() differs
    """
    def letterCasePermutation(self, S: str):
        rv = []
        self.recur(S, "", 0, rv)
        return rv

    def recur1(self, s, curr_str, rv):
        if len(curr_str) == len(s):
            rv.append(curr_str)
            return
        for i in range(len(curr_str), len(s)):
            if s[i].isdigit():
                self.recur1(s, curr_str + s[i], rv)
            else:
                self.recur1(s, curr_str + s[i].upper(), rv)
                self.recur1(s, curr_str + s[i].lower(), rv)

    def recur(self, s, curr_str, curr_i, rv):
        if len(curr_str) == len(s):
            rv.append(curr_str)
            return
        for i in range(curr_i, len(s)):
            if s[i].isdigit():
                self.recur(s, curr_str + s[i], i + 1, rv)
            else:
                self.recur(s, curr_str + s[i].upper(), i + 1, rv)
                self.recur(s, curr_str + s[i].lower(), i + 1, rv)


class Solution854:
    """
    Strings A and B are K-similar (for some non-negative integer K) if we can swap the positions of two letters in A exactly K times so that the resulting string equals B.
    Given two anagrams A and B, return the smallest K for which A and B are K-similar.
    Example
    A = aebdc, B = dceba, return 4

    BFS solution
    For the i-th char in A, find its one swap neighbors, i.e., all strings after swapping in the correct i-th char (B[i])
    Now the i-th position is done, find the next position that is not the correct char (B[i])
    Repeat the procedure, keep track of the cost, every time visiting, cost increment by 1 from the cost of the input string
    """

    def kSimilarity(self, A: str, B: str):
        if sorted(A) != sorted(B):
            return float("inf")

        def bfs_one_swap_neighbors(s):
            neighbors = []
            for i, c in enumerate(s):
                if c != B[i]: break
            s = list(s)
            for j in range(i + 1, len(s)):
                if B[i] == s[j]:
                    s[j], s[i] = s[i], s[j]
                    neighbors.append("".join(s))
                    s[j], s[i] = s[i], s[j]
            return neighbors

        queue = collections.deque([(A, 0)])
        visited = set()
        while queue:
            curr_s, cost = queue.popleft()
            if curr_s == B: return cost
            ns = bfs_one_swap_neighbors(curr_s)
            visited.add(curr_s)
            for s in ns:
                if s not in visited:
                    queue.append((s, cost + 1))


class Solution1147:
    """
    Return the largest possible k such that there exists a_1, a_2, ..., a_k such that:
    Each a_i is a non-empty string;
    Their concatenation a_1 + a_2 + ... + a_k is equal to text;
    For all 1 <= i <= k,  a_i = a_{k+1 - i}.
    Input: text = "ghiabcdefhelloadamhelloabcdefghi"
    Output: 7
    Explanation: We can split the string on "(ghi)(abcdef)(hello)(adam)(hello)(abcdef)(ghi)".

    Rolling hash + two pointers solution
    compute rhash for strings starting at the pointers
    once found a match, clear hashes to 0 and increment results
    """
    def longestDecomposition(self, text: str) -> int:
        n = len(text)
        p1, p2 = 0, n-1
        ans = 0
        hl, hr, hr_pow = 0, 0, 1
        base, p = 128, 10 ** 9 + 7
        while p1 <= p2:
            hl = (ord(text[p1]) + (hl * (base)) % p) % p
            hr = (hr + (ord(text[p2]) * hr_pow ) % p ) % p
            hr_pow *= base % p
            if hl == hr:
                # BUG: not check string equals since p is relatively large
                ans += 2 if p1 != p2 else 1 # corner cases: if hashes are equal when sharing the middle letter
                hl, hr, hr_pow = 0, 0, 1
            p1 += 1
            p2 -= 1
        if hl > 0: ans += 1 # corner cases: if there is a middle string left
        return ans


class Solution761:
    """
    Special binary strings are binary strings with the following two properties:
    - The number of 0's is equal to the number of 1's.
    - Every prefix of the binary string has at least as many 1's as 0's.
    Given a special string S, a move consists of choosing two consecutive, non-empty, special substrings of S, and swapping them.
    (Two strings are consecutive if the last character of the first string is exactly one index before the first character of the second string.)
    At the end of any number of moves, what is the lexicographically largest resulting string possible?
    Example.
    Input: S = "11011000"
    Output: "11100100"
    Explanation:
    The strings "10" [occurring at S[1]] and "1100" [at S[3]] are swapped.
    This is the lexicographically largest string possible after some number of swaps.

    If we regard 1, 0 in the definition of the special string as '(' and ')' separately,
    the problem is actually to get the string which is so-called valid parenthesis and meanwhile is the lexicographically largest.
    We prefer deeper valid parenthesis to sit in front, deeper means the string surrounded with more pairs of parenthesis, e.g., '(())' is deeper than '()'.
    We can achieve that by sorting them reversely.
    we go through S. Whenever the parentheses we met can be balanced (i.e., balance == 0), we construct valid parentheses -- by putting '(' on the left boundary, ')' on the right boundary, and doing with the inner part following the same pattern.
    """
    def makeLargestSpecial(self, S: str) -> str:
        balance, left = 0, 0
        ordered_special_substrings = []
        for right in range(0, len(S)):
            balance += 1 if S[right] == "1" else -1
            if balance == 0:
                # if the inner part is lexicographically largest possible, then the outer string will be too
                # iterating the substrings from left to right and branch once we see balanced 1s and 0s
                # this ensures that we only touch consecutive special substrings
                # i.e., "1010" will be processed as  "10" and "10", so "1100" is not possible
                ordered_substring = "1" + self.makeLargestSpecial(S[left+1:right]) + "0"
                ordered_special_substrings.append(ordered_substring)
                left = right + 1
        ordered_special_substrings.sort(reverse=True)
        return "".join(ordered_special_substrings)
