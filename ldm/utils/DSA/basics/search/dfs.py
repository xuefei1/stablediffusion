from typing import List


def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    res = []

    def dfs(_target, index, path):
        if _target < 0:
            return  # backtracking
        if _target == 0:
            res.append(path)
            return
        for i in range(index, len(candidates)):
            dfs(_target - candidates[i], i, path + [candidates[i]])

    dfs(target, 0, [])
    return res
