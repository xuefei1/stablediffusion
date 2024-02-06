


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution971:
    """
    Flip Binary Tree To Match Pre-order Traversal
    Given a binary tree with N nodes, each node has a different value from {1, ..., N}.
    A node in this binary tree can be flipped by swapping the left child and the right child of that node.
    Consider the sequence of N values reported by a pre-order traversal starting from the root.
    Call such a sequence of N values the voyage of the tree.
    (Recall that a preorder traversal of a node means we report the current node's value, then preorder-traverse the left child, then preorder-traverse the right child.)
    Our goal is to flip the least number of nodes in the tree so that the voyage of the tree matches the voyage we are given.
    If we can do so, then return a list of the values of all nodes flipped.  You may return the answer in any order.
    If we cannot do so, then return the list [-1].
    """
    def flipMatchVoyage(self, root: TreeNode, voyage):
        self.ans = []
        self.i = 0

        def traverse(node):
            if node is None:
                return
            if node.val != voyage[self.i]:
                self.ans = [-1]
                return
            self.i += 1
            if node.left is not None and node.left.val != voyage[self.i]:
                self.ans.append(node.val)
                traverse(node.right)
                traverse(node.left)
            else:
                traverse(node.left)
                traverse(node.right)

        traverse(root)
        if len(self.ans) > 0 and self.ans[0] == -1:
            self.ans = [-1]
        return self.ans