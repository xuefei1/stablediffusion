"""
Always go for the best possible result so far. Do not care about global optimal.
The greedy strategy design also has a major impact on whether the optimal can be found greedily.
Dijkstra's algorithm is based on a greedy strategy.
Main advantage of greedy algorithm is to save time, don't need to iterate all possibilities.
"""


def min_number_of_coins_to_pay(target, coins=(100,50,10,5,1)):
    """
    Whether greedy approach can find the optimal solution is dependent on the type of coins.
    """
    ret = 0
    index = 0
    while target > 0 and index < len(coins):
        ret += target / coins[index]
        target %= coins[index]
        index += 1
    return ret
