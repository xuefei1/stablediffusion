from basics.bits.msb_of import msb_of

"""
A segment tree is used to speed up range search for an array of numbers
e.g., find the min within index range [2,4]

O(n) create time, O(n) space to maintain, O(log n) query time

The leaf node will be numbers in the array, non-leaf node will be purpose-specific values
in the case of finding the min within an range, parent node will be the min among all its leaf nodes

To create a segment tree, first divide the array in half, continue doing so until there are 2 or 1 or 0 number(s)
left in each group, these will be the leaf node, for a single number, it will be one level higher than 2 numbers

Segment tree is a full binary tree, every node other than leaf have two children

For arrays with n elements, there will be at most 2m-1 number of tree nodes, where m is the next power of 2 for n,
if n == 5, m = 8 = 2^3

For example, to create an segment tree for -1,3,4,0,2,1 to find the min within an range

                    -1 min value in range [0,5]
                /          \
              -1[0,2]      0[3,5]
            /     \         /     \
        -1[0,1]  4[2,2]  0[3,4]   1[5,5]
       /     \         /     \
    -1[0,0]  3[1,1]   0[0,0]  2[1,1]

To query the min given a range[2,4], we check three cases:
1. if given range partial overlaps the current node range, recursively check left/right child
2. if given range totally contains the current node range, return the current node min to previous calls
3. if given range does not overlap the current node range at all, return MAX int (impossible value, outside range)

In each recursive call, compare to find min

To represent a segment tree using an array, allocate 2m-1 positions, m is the next power of 2
left child = 2 * i + 1, right child = 2 * i + 2, parent = (i - 1) // 2, same as binary heap
left child keeps first half of the range indicated by parent node [low, mid] of tree array
right child keeps the second half [mid + 1, high]
this way, actual array elements will always appear at the end of the array
"""
class MinSegmentTree:

    def __init__(self, arr):
        self.arr_len = len(arr)
        self.tree = [float("inf")] * (2*next_power_of_2(len(arr))-1)

    def make_tree_recursive(self, arr, curr_i, lo, hi):
        if lo == hi:
            self.tree[curr_i] = arr[lo]
            return
        mid = lo + (hi - lo) // 2
        self.make_tree_recursive(arr, 2 * curr_i + 1, lo, mid)
        self.make_tree_recursive(arr, 2 * curr_i + 2, mid, hi)
        self.tree[curr_i] = min(self.tree[2 * curr_i + 1], self.tree[2 * curr_i + 2])

    def range_query_min(self, lo, hi):
        return self._range_query_min_recursive(lo, hi, 0, self.arr_len-1, 0)

    def _range_query_min_recursive(self, qry_lo, qry_hi, curr_lo, curr_hi, curr_i):
        # total containment
        if qry_lo <= curr_lo and qry_hi >= curr_hi:
            return self.tree[curr_i]
        # no overlap
        if qry_lo > curr_hi or qry_hi < curr_lo:
            return float("inf")
        # partial overlap
        mid = curr_lo + (curr_hi - curr_lo) // 2
        left_min = self._range_query_min_recursive(qry_lo, qry_hi, curr_lo, mid, 2 * curr_i + 1)
        right_min = self._range_query_min_recursive(qry_lo, qry_hi, mid + 1, curr_hi, 2 * curr_i + 2)
        return min(left_min, right_min)


def next_power_of_2(num):
    return 1 << (msb_of(num) + 1)


if __name__ == "__main__":
    print(next_power_of_2(5))
