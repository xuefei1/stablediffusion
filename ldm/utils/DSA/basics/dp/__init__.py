"""
If the problem involves make k choices for n steps. Then the brute force complexity is O(k**n).
Top down with memo could given O(n) time O(n) space.
Bottom up DP could have O(n) time O(1) space, depending on the problem.

DP is often used in problems involving finding extremes: "best", "fewest", "longest"
- The optimal solution's sub-solution is also the optimum.
- Once the optimal sub-solution is found it will not be affected by future bigger solutions.
- Sub problems contain many overlapping cases, so a table is needed.
"""


def max_profit_from_cut(L, prices):
    """
    Given steel of length L and prices for different length.
    Find the max possible money we can make by cutting.
    If prices dict has size m, only need to track m most recent results.
    Since the order of cut does not matter, only need to memo the last cut, which has to give a size within prices and a remaining size.
    O(Lm) time, O(m) space in the optimal case.
    """
    m = len(prices)
    memo = [0] * (L + 1)
    for n in range(L + 1):
        if n in prices:
            memo[n] = prices[n]
        if n > 1:
            for k in range(min(m, n)):
                # Last cut must give a length within m
                value = memo[k] + memo[n-k]
                memo[n] = max(memo[n], value)
        # TODO space complexity is not optimal here
    return memo


if __name__ == "__main__":
    print(max_profit_from_cut(13, {0:0,1:1,2:5,3:8,4:9,5:10,6:17,7:17,8:20,9:24,10:30}))
