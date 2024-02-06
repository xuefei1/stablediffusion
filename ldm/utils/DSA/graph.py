import collections


def numIslands(grid) -> int:
    """
    Number of islands
    Given a 2d grid map of '1's (land) and '0's (water), count the number of islands.
    An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.
    You may assume all four edges of the grid are all surrounded by water.

    O(VE) time and space
    DFS
    """
    rv = 0
    visited = [[False for _ in row] for row in grid]
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            found_new = recurFind(grid, r, c, visited)
            if found_new:
                rv += 1
    return rv

def recurFind(mat, r, c, visited):
    if visited[r][c]: return False
    visited[r][c] = True
    if mat[r][c] == "0":
        return False
    if r - 1 >= 0:
        recurFind(mat, r- 1, c, visited)
    if r + 1 < len(mat):
        recurFind(mat, r + 1, c, visited)
    if c - 1 >= 0:
        recurFind(mat, r, c - 1, visited)
    if c + 1 < len(mat[0]):
        recurFind(mat, r, c + 1, visited)
    return True


def findLadders(beginWord, endWord, wordList):
    """
    Word Ladder II
    Given two words (beginWord and endWord), and a dictionary's word list, find all shortest transformation sequence(s) from beginWord to endWord, such that:
    Only one letter can be changed at a time
    Each transformed word must exist in the word list. Note that beginWord is not a transformed word.

    Input:
    beginWord = "hit",
    endWord = "cog",
    wordList = ["hot","dot","dog","lot","log","cog"]
    Output:
    [
      ["hit","hot","dot","dog","cog"],
      ["hit","hot","lot","log","cog"]
    ]
    BFS + BackTrack
    """
    wordList.append(beginWord)
    adj_lists = buildAdjListGraph(wordList)
    q = [beginWord]
    visited = set()
    min_steps = None
    n_steps = 0
    while len(q) > 0:
        tmp = []
        for word in q:
            if word == endWord:
                min_steps = n_steps + 1 if min_steps is None else min(min_steps, n_steps + 1)
            else:
                for neighbor in adj_lists[word]:
                    if neighbor not in visited:
                        tmp.append(neighbor)
        for word in q:
            visited.add(word)
        n_steps += 1
        q = tmp
    if min_steps is None: return []
    print("min steps: {}".format(min_steps))
    rv = []
    backTrackFindLadders([beginWord], beginWord, adj_lists, rv, min_steps, endWord)
    return rv

def backTrackFindLadders(currPathList, word, graph, rv, n_steps, tgt_word):
    if len(currPathList) == n_steps:
        if currPathList[-1] == tgt_word:
            rv.append([w for w in currPathList])
        return
    for neighbor_word in graph[word]:
        currPathList.append(neighbor_word)
        backTrackFindLadders(currPathList, neighbor_word, graph, rv, n_steps, tgt_word)
        del currPathList[-1]

def buildAdjListGraph(wordList):
    rv = {}
    for i, tgt_word in enumerate(wordList):
        rv[tgt_word] = set()
        for j, cmp_word in enumerate(wordList):
            if i == j: continue
            if not isOneEditAway(tgt_word, cmp_word): continue
            rv[tgt_word].add(cmp_word)
    return rv

def isOneEditAway(str1, str2):
    return len([1 for i in range(len(str1)) if str1[i] != str2[i]]) == 1


def wordBreak(s: str, wordDict):
    """
    Word Break II
    Given a non-empty string s and a dictionary wordDict containing a list of non-empty words, add spaces in s to construct a sentence where each word is a valid dictionary word.
    Return all such possible sentences.

    Input:
    s = "catsanddog"
    wordDict = ["cat", "cats", "and", "sand", "dog"]
    Output:
    [
      "cats and dog",
      "cat sand dog"
    ]
    """
    rv = []
    wordDict = set(wordDict)
    valid_substring_set = {""}
    for i in range(len(s) - 1, -1, -1):
        for j in range(i, len(s)):
            word = s[i:j + 1]
            if len(word) == 0: continue
            if word in wordDict and s[j + 1:] in valid_substring_set:
                valid_substring_set.add(s[i:])
    # print(valid_substring_set)
    backTrackWordBreak([], s, wordDict, rv, valid_substring_set)
    return rv

def backTrackWordBreak(curr_seq, remain_seq, word_set, rv, valid_substring_set):
    if len(remain_seq) == 0:
        rv.append(" ".join(curr_seq))
        return
    if remain_seq not in valid_substring_set:
        return
    tmp = []
    for i, c in enumerate(remain_seq):
        tmp.append(c)
        key = "".join(tmp)
        if key in word_set:
            curr_seq.append(key)
            backTrackWordBreak(curr_seq, remain_seq[i + 1:], word_set, rv, valid_substring_set)
            del curr_seq[-1]


def possibleBipartition(N, dislikes):
    """
    Possible Bipartition
    Given a set of N people (numbered 1, 2, ..., N), we would like to split everyone into two groups of any size.
    Each person may dislike some other people, and they should not go into the same group.
    Formally, if dislikes[i] = [a, b], it means it is not allowed to put the people numbered a and b into the same group.
    Return true if and only if it is possible to split everyone into two groups in this way.

    There cannot be an odd-cycle in the dislikes graph, if yes -> not possible
    A cyclic graph is bipartite iff all its cycles are of even length (Skiena 1990, p. 213)

    Best solution:
    Time Complexity: O(N + E) E is the length of dislikes
    Space Complexity: O(N + E)
    For each connected component, we can check whether it is bipartite by just trying to coloring it with two colors.
    How to do this is as follows: color any node red, then all of it's neighbors blue, then all of those neighbors red, and so on.
    If we ever color a red node blue (or a blue node red), then we've reached a conflict.
    """
    graph = collections.defaultdict(list)
    for u, v in dislikes:
        graph[u].append(v)
        graph[v].append(u)

    color = {}

    def dfs(node, c=0):
        if node in color:
            return color[node] == c
        color[node] = c
        return all(dfs(neighbor, c ^ 1) for neighbor in graph[node])

    return all(dfs(node) for node in range(1, N + 1) if node not in color)


class Solution787:
    """
    There are n cities connected by m flights. Each fight starts from city u and arrives at v with a price w.
    Now given all the cities and flights, together with starting city src and the destination dst, your task is to find the cheapest price from src to dst with up to k stops.
    If there is no such route, output -1.
    """
    def findCheapestPrice(self, n: int, flights, src: int, dst: int, K: int) -> int:
        import heapq
        graph = collections.defaultdict(set)
        for s,dest,cost in flights:
            graph[s].add((dest, cost))
        q = [(0, src, 0)]
        heapq.heapify(q)
        while q:
            cost, city, k = heapq.heappop(q)
            if city == dst:
                return cost
            if k > K: continue
            for n, c in graph[city]:
                heapq.heappush(q, (c+cost, n, k+1))
        return -1

