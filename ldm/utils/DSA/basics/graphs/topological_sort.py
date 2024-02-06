"""
Topological ordering
Find an ordering of nodes such that, for any edge u-v within a directed acyclic graph (DAG)
u always comes before v in the final ordering result -- dependency enforcement
There is more than 1 possible ordering

Solution 1. DFS
For each unvisited vertex, add it to visited set
Then add all its children to visited, then each child do the same thing
When we found a node with no more child, or finished with all children of a node, add this node to result

Solution 2. Khan's algorithm (in/out degrees)
Compute the indegrees of each node
Find nodes without any indegree, remove them from the indegree lists of other nodes
Repeat above step
"""
def topological_dfs(adj_list):
    # adj_list: [[1,2,3], [0,4], ...], i.e., node 0 has edge to 1,2,3, node 1 has edge 0,4.
    visited = set()
    result = []

    def dfs(n):
        visited.add(n)
        for child in adj_list[n]:
            if child not in visited:
                dfs(child)
        result.append(n)

    for v in range(len(adj_list)):
        if v not in visited:
            dfs(v)
    return result[::-1]


def topological_khan(adj_list):
    # adj_list: [[1,2,3], [0,4], ...], i.e., node 0 has edge to 1,2,3, node 1 has edge 0,4.
    in_degrees = [0 for _ in adj_list]
    for n1 in in_degrees:
        for n2 in adj_list[n1]:
            in_degrees[n2] += 1
    remain_set = set([n for n in range(len(adj_list))])
    rv = []
    for n, nd in enumerate(in_degrees):
        if nd == 0:
            rv.append(n)
            remain_set.remove(n)
    while len(remain_set) > 0:
        for n, _ in enumerate(in_degrees):
            if n not in remain_set: continue
            for v in adj_list[n]:
                if v not in remain_set:
                    in_degrees[n] -= 1
                    if in_degrees[n] == 0:
                        rv.append(n)
                        remain_set.remove(n)
    return rv
