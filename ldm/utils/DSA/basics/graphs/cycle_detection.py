"""
Undirected graph cycle detection

Solution 1. Disjoint Set
Create a set for each node, then when visiting the next node, union it with the current node if they have different parents,
if two node you are about the union have the same parent node, there is a cycle in the graph
O(v) time, v is the number of vertices

Solution 2. DFS
For each node find its neighbors
for each neighbor, if the neighbor is not the parent of the current node, i.e. the node that we reached current node from
and it's already in a visited set, return true
Running time/space both O(v), v is the number of vertices
"""
def has_cycle_undirected_union_find(vertex_set, edges):
    from basics.sets.disjoint_set import DisjointSet
    ds = DisjointSet()
    for v in vertex_set:
        ds.make_set(v)
    for src, dst in edges:
        parent1 = ds.find_set_rep(src)
        parent2 = ds.find_set_rep(dst)
        if parent1 == parent2:
            return True
        ds.union(src, dst)
    return False

def has_cycle_undirected_dfs(adj_list):
    # adj_list: [[1,2,3], [0,4], ...], i.e., node 0 has edge to 1,2,3, node 1 has edge 0,4.
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in adj_list[node]:
            if neighbor in visited and neighbor != parent:
                return True
            elif neighbor not in visited and dfs(neighbor, node):
                return True
        return False

    for n in range(len(adj_list)):
        if n not in visited and dfs(n, -1):
            return True
    return False


"""
Directed graph cycle detection

Solution 1. 3-set DFS
Maintain 3 sets, white set hold vertices not visited, gray set holds vertices currently visiting, and black set holds visited vertices
Start at any point, recursive all neighbors, when find a neighbor in gray set, return true
When finished loop in recursive call i.e., visited all the neighbors, add the current node to the black set
"""
def has_cycle_directed_dfs(adj_list):
    white_set, gray_set, black_set = set(), set(), set()
    for n in range(len(adj_list)):
        white_set.add(n)

    def dfs(cur):
        white_set.remove(cur)
        gray_set.add(cur)
        for neighbor in adj_list[cur]:
            if neighbor in black_set: continue
            if neighbor in gray_set: return True
            if dfs(neighbor): return True
        gray_set.remove(cur)
        black_set.add(cur)
        return False

    while len(white_set) > 0:
        node = white_set.pop()
        if dfs(node): return True
    return False


