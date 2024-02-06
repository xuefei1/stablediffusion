import collections
from functools import lru_cache


class Solution464:
    """
    In the "100 game," two players take turns adding, to a running total, any integer from 1..10. The player who first causes the running total to reach or exceed 100 wins.
    What if we change the game so that players cannot re-use integers?
    For example, two players might take turns drawing from a common pool of numbers of 1..15 without replacement until they reach a total >= 100.
    Given an integer maxChoosableInteger and another integer desiredTotal, determine if the first player to move can force a win, assuming both players play optimally.
    You can always assume that maxChoosableInteger will not be larger than 20 and desiredTotal will not be larger than 300.
    """
    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        if (1 + maxChoosableInteger) * maxChoosableInteger / 2 < desiredTotal:
            return False
        return self.recurCompute(0, [n for n in range(1, maxChoosableInteger + 1)], desiredTotal, {})

    def recurCompute(self, curr_total, curr_ints, desiredTotal, memo):
        key = tuple(curr_ints)
        if key in memo:
            return memo[key]
        for i, n in enumerate(curr_ints):
            if n + curr_total >= desiredTotal:
                # player1 win if any pick lead player1 to reach the goal
                memo[key] = True
                return True
            if not self.recurCompute(curr_total + n, curr_ints[:i] + curr_ints[i + 1:], desiredTotal, memo):
                # player1 win if any pick lead player2 to lose
                memo[key] = True
                return True
        # otherwise player1 lose
        memo[key] = False
        return memo[key]


class Solution1178:
    """
    With respect to a given puzzle string, a word is valid if both the following conditions are satisfied:
    word contains the first letter of puzzle.
    For each letter in word, that letter is in puzzle.
    For example, if the puzzle is "abcdefg", then valid words are "faced", "cabbage", and "baggage"; while invalid words are "beefed" (doesn't include "a") and "based" (includes "s" which isn't in the puzzle).
    Return an array answer, where answer[i] is the number of words in the given word list words that are valid with respect to the puzzle puzzles[i].

    The key is to create all possible combinations of letter bits for letters in each puzzle
    Since len(puzzle) = 7, this is fast
    """
    def findNumOfValidWords(self, words, puzzles):
        word_count = collections.defaultdict(int)
        for word in words:
            bits = 0
            word = set(word)
            if len(word) > 7: continue
            for c in word:
                bits |= 1<<(ord(c)-ord('a'))
            word_count[bits] += 1
        rv = []
        for puzzle in puzzles:
            # build all possible puzzle letter combinations using bit masks
            possible_bits = [1 << (ord(puzzle[0])-ord('a'))]
            for c in puzzle[1:]:
                tmp = []
                for curr_bits in possible_bits: # This is fast because puzzle len = 7
                    new_bits = curr_bits | 1 << (ord(c)-ord('a'))
                    tmp.append(new_bits)
                possible_bits.extend(tmp)
            rv.append(sum(word_count[b] if b in word_count else 0 for b in possible_bits))
        return rv


class Solution913:
    """
    Cat Mouse Game
    A game on an undirected graph is played by two players, Mouse and Cat, who alternate turns.
    The graph is given as follows: graph[a] is a list of all nodes b such that ab is an edge of the graph.
    Mouse starts at node 1 and goes first, Cat starts at node 2 and goes second, and there is a Hole at node 0.
    During each player's turn, they must travel along one edge of the graph that meets where they are.  For example, if the Mouse is at node 1, it must travel to any node in graph[1].
    Additionally, it is not allowed for the Cat to travel to the Hole (node 0.)

    Then, the game can end in 3 ways:
        If ever the Cat occupies the same node as the Mouse, the Cat wins.
        If ever the Mouse reaches the Hole, the Mouse wins.
        If ever a position is repeated (ie. the players are in the same position as a previous turn, and it is the same player's turn to move), the game is a draw.
    Given a graph, and assuming both players play optimally, return 1 if the game is won by Mouse, 2 if the game is won by Cat, and 0 if the game is a draw.

    DP solution run time O(N^3), since there are 2*n*n*n possible states, memo ensures each state is visited once.
    """
    def catMouseGame(self, graph) -> int:
        return self.search(graph, state=(0, 1, 2), isMouseMove=True, memo={})

    def search(self, graph, state, isMouseMove, memo):
        time, mouse_loc, cat_loc = state
        # base cases
        if mouse_loc == 0: return 1  # mouse in hole, mouse wins
        if mouse_loc == cat_loc: return 2  # cat mouse at one node, cat wins
        if time == 2 * len(
            graph): return 0  # game continued for more than 2*n, meaning we now have to go back to a  visited node, end in a draw
        if state in memo: return memo[state]  # already computed value for this state, return

        if isMouseMove:  # mouse's move
            # visit neighboring nodes, update state
            # if any subsequent search returns 1, return 1
            # if all subsequent searches return 2, return 2, no way to win
            # else, eventually sub-calls will return 0, also return 0 here
            # in all cases, we need to store the results in memo
            subsequent_vals = []
            for n in graph[mouse_loc]:
                val = self.search(graph, (time + 1, n, cat_loc), not isMouseMove, memo)
                if val == 1:
                    memo[state] = 1
                    return 1
                subsequent_vals.append(val)
            if all(v == 2 for v in subsequent_vals):
                memo[state] = 2
            else:
                memo[state] = 0
        else:  # cat's move
            # visit neighboring nodes, update state
            # if any subsequent search returns 2, return 2
            # if all subsequent searches return 1, return 1
            subsequent_vals = []
            for n in graph[cat_loc]:
                if n == 0: continue  # cat cannot go to node 0
                val = self.search(graph, (time + 1, mouse_loc, n), not isMouseMove, memo)
                if val == 2:
                    memo[state] = 2
                    return 2
                subsequent_vals.append(val)
            if all(v == 1 for v in subsequent_vals):
                memo[state] = 1
            else:
                memo[state] = 0
        return memo[state]


class Solution486:
    """
    Given an array of scores that are non-negative integers.
    Player 1 picks one of the numbers from either end of the array followed by the player 2 and then player 1 and so on.
    Each time a player picks a number, that number will not be available for the next player.
    This continues until all the scores have been chosen. The player with the maximum score wins.
    Given an array of scores, predict whether player 1 is the winner. You can assume each player plays to maximize his score.

    O(n^2) time and space DP
    To win need score1 >= score2, or score1 - score2 >= 0
    memo[i][j] represents the best advantage of the current acting player over the other player for the sub-array starting at i and ending at j inclusive
    memo[i][i] = nums[i], meaning player 2 has nothing to choose, so advantage is nums[i] - 0
    for 2-element arrays, player 1's best advantage over player 2 will be max(nums[i] - memo[i+1][i], nums[i+1] - memo[i][i-1])
    i.e., choose left or right element, whichever gives the most advantage
    for 3-element arrays, player 1's best advantage over player 2 will be max(nums[i] - memo[i+1][j], nums[j] - memo[i][j-1])
    **i.e., when the first player chooses nums[i], memo[i+1][j] will be the opponent's best achievable advantage, which is why it is a "-"**
    by choosing this element, if we can still maintain a non-negative advantage, then it is good.
    similarly for when choosing nums[j]
    """
    def PredictTheWinner(self, nums) -> bool:
        memo = [[0] * len(nums)] * len(nums)
        for s in range(len(nums)-1, -1, -1):
            memo[s][s] = nums[s]
            for e in range(s+1, len(nums)):
                lv = nums[s] - memo[s+1][e]
                rv = nums[e] - memo[s][e-1]
                memo[s][e] = max(lv, rv)
        return memo[0][len(nums)-1] >= 0


class Solution1027:
    """
    Longest Arithmetic Sequence
    Given an array A of integers, return the length of the longest arithmetic subsequence in A.
    Recall that a subsequence of A is a list A[i_1], A[i_2], ..., A[i_k] with 0 <= i_1 < i_2 < ... < i_k <= A.length - 1, and that a sequence B is arithmetic if B[i+1] - B[i] are all the same value (for 0 <= i < B.length - 1).

    O(N^2) DP
    for a position j, compute diff A[j] - A[i] for all i before j
    if A[j] - A[i] already gives part of a subsequence candidate, add 1 to its existing length
    else, initialize it to be 1, i.e., now there is a subsequence candidate with 2 elements and diff = A[j] - A[i], [A[i], A[j]]
    track the running max along the way
    """
    def longestArithSeqLength(self, A) -> int:
        memo = [collections.defaultdict(int) for _ in A]
        ans = 0
        for i in range(1, len(A)):
            for j in range(0, i):
                diff = A[j] - A[i]
                memo[i][diff] = memo[j][diff] + 1
                ans = max(ans, memo[i][diff])
        return ans + 1


class Solution903:
    """
    Valid Permutations for DI Sequence
    We are given S, a length n string of characters from the set {'D', 'I'}. (These letters stand for "decreasing" and "increasing".)
    A valid permutation is a permutation P[0], P[1], ..., P[n] of integers {0, 1, ..., n}, such that for all i:
    If S[i] == 'D', then P[i] > P[i+1], and;
    If S[i] == 'I', then P[i] < P[i+1].
    How many valid permutations are there?  Since the answer may be large, return your answer modulo 10^9 + 7.

    O(N^3) DP
    Given a position, a chosen number from 0 to n, and the letter D or I, we know what other numbers can be chosen for the next position
    We work backwards from the last char.
    For the last position, there are n+1 possible choices of numbers, although some of them won't be possible depending on the actual char
    We sum the results of all these choices, given a choice P_i, the preceding position could have these choices:
     - If the char is D, then the previous number must be greater than the current number, so it can be from P_i to n
     - If the char is I, the previous number could be from 0 to P_i not including P_i
    We memoize the results of shorter prefixes according to:
     1. the length of the prefix
     2. the number placed at the current position, i.e., its relative rank
    dp[i][j] stores how many ways to place the number j at the i-th position, such that the sequence satisfies the input S
    Base case is when there is no preceding number, hence there is only 1 way to put j
    For the i-th position, we need to add the results from all possible numbers to put there depending on the previous number (j), and whether the char is D or I
    """
    def numPermsDISequence(self, S):
        MOD = 10**9 + 7
        N = len(S)

        @lru_cache(None)
        def dp(i, j):
            # How many ways to place P_i with relative rank j?
            if i == 0:
                return 1
            # For the i-th position, we need to add the results from all possible numbers to put there depending on the previous number (j), and whether the char is D or I
            elif S[i-1] == 'D':
                return sum(dp(i-1, k) for k in range(j, i)) % MOD
            else:
                return sum(dp(i-1, k) for k in range(j)) % MOD

        return sum(dp(N, j) for j in range(N+1)) % MOD
