"""
BFS is often used to solve problems involving "shortest", "smallest", "fastest".
BFS could take more memory than DFS, so it's not suitable for counting questions like "find the total number of ways to reach somewhere".
BFS LC 102, 787, 909, 127

DFS can be used to solve the classic N-queens problem.
O(n!) time complexity.
DFS is commonly combined with recursion and backtrack.
DFS can also be used to find if a certain sequence exists in a graph.
DFS LC 94, 133, 365, 437
"""


def bfs_shortest_path_mat(mat, sr, sc, tr, tc):
    """
    Mat value = 0 means the cell is blocked.
    Only can move up/down/left/right.
    """
    q = [(sr, sc, 0)]
    while q:
        r, c, s = q.pop(0)
        s += 1
        if r == tr and c == tc:
            return s
        if r > 0 and mat[r-1][c] > 0:
            q.append((r-1, c, s))
            mat[r-1][c] = -1
        if c > 0 and mat[r][c-1] > 0:
            q.append((r, c-1, s))
            mat[r][c-1] = -1
        if r < len(mat) - 1 and mat[r+1][c] > 0:
            q.append((r+1, c, s))
            mat[r+1][c] = -1
        if c < len(mat[0]) and mat[r][c+1] > 0:
            q.append((r, c+1, s))
            mat[r][c+1] = -1
    return None


def n_queens(n_queen):
    """
    How many different ways to arrange n queens such that no queen attack others.
    """
    ret = 0
    # Pos represents different columns, the number at i means queen placed at row i
    pos = [0] * (n_queen + 1) # First index not used for simpler logic

    def is_valid_pos(step, p):
        nonlocal pos
        for i in range(1, step):
            if p == pos[i]: # Check for same row
                return False
            if p - step == pos[i] - i: # Check for angle attacks
                return False
            if p + step == pos[i] + i: # Check for angle attacks
                return False
        return True

    def dfs(step):
        nonlocal pos
        nonlocal ret
        if step > n_queen:
            ret += 1
            return
        for i in range(1, n_queen + 1):
            if is_valid_pos(step, i):
                pos[step] = i
                dfs(step + 1)
                pos[step] = 0
    dfs(1)
    return ret


if __name__ == "__main__":
    print(n_queens(9))
