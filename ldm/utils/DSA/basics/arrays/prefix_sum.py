"""
Prefix sum is useful for solving interval sum problems.
E.g., find sub-array in array with max sum, or find sub-matrix in matrix with max sum.
LC 209, 238, 560, 304, 1991
"""


def mat_pre_sum(mat, i, j):
    s1 = mat[i][j]
    s2 = mat[i][j-1] if j > 0 else 0
    s3 = mat[i-1][j] if i > 0 else 0
    s4 = mat[i-1][j-1] if i > 0 and j > 0 else 0
    return s1 + s2 + s3 - s4


def sub_mat_sum(pre_sum_mat, x, y, m, n):
    s1 = pre_sum_mat[x][y]
    s2 = pre_sum_mat[x][y - n] if y >= n else 0
    s3 = pre_sum_mat[x - m][y] if x >= m else 0
    s4 = pre_sum_mat[x - m][y - n] if y >= n and x >= m else 0
    return s1 - s2 - s3 + s4
