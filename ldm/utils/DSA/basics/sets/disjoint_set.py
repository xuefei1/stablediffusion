
"""
Also called Union Find

Implements two operations, union and find

contains multiple subsets, each has a unique representative, call findSet()
on any of its member will return the representative

Time complexity for disjoint set is O( m x alpha(n)) where m is the number of operations
and n is the number of nodes, alpha is a slowly growing function alpha(n) <= 4
"""
class DisjointSetNode:

    def __init__(self, data, rank=0):
        self.rank = rank
        self.data = data
        self.parent_node = self

class DisjointSet:

    def __init__(self):
        self.val2node = {}

    def make_set(self, data):
        if data not in self.val2node:
            node = DisjointSetNode(data)
            self.val2node[data] = node

    def union(self, data1, data2):
        node1 = self.val2node[data1]
        node2 = self.val2node[data2]

        parent1 = self.find_set_rep(node1)
        parent2 = self.find_set_rep(node2)
        if parent1.data == parent2.data:
            return # if they are in the same set

        if parent1.rank == parent2.rank:
            # if they have the same rank, merge them and increase rank by 1
            parent2.parent_node = parent1
            parent1.rank += 1
        elif parent1.rank > parent2.rank:
            # the set that has the higher rank will be the parent
            parent2.parent_node = parent1
        else:
            parent1.parent_node = parent2

    def find_set_rep(self, node):
        if node.parent_node is node:
            return node # if parent == itself, we found the representative
        # else we need to keep going up the chain
        # meanwhile we need to reset the current node's parent to the node that satisfied the base case
        # i.e., we are shorting the distance to representative node (path compression)
        node.parent_node = self.find_set_rep(node.parent_node)
        return node.parent_node
