import collections

"""
A Trie is a tree-like data structure where parent and child have the same prefixes
Example: thd, te, afg, alo, ivs
                   t,a,i
              t/    a|    i\
            h,e     f,l    v
           h/ \e   f| |l    v\
           d       g o       s

Insertion time O(l n) l is the average length of the words, n is the number of words to insert
Look up time O(l), l is the length of the word to search for
Deletion time O(l), l is the length of the word to delete

Insert:
Start with root, check if root node map contains the first char
if yes, then move on the second char and next node.
if no, create new key using first char and put empty node in, check if end of word to determine the flag value, move on to next node

Search with prefix:
Start with root, check if root contains the first char, if not return false, else move on to the next node and check for next char

Search whole word:
Recursively check if each char exists, once reached the last char, check if it's children isEndOfWord

Delete whole word:
1. Find the word by searching all the way to the last character
2. Check its children is empty, if not, simply turn off the isEndOfWord flag on its children
  If children is empty, delete this key and children, repeat the checking on its parent node

Delete by prefix:
  Simply find the prefix, then clear its children's map, repeat the checking on its parent node
"""
class TrieNode:

    def __init__(self):
        self.is_end_of_word = False
        self.children = collections.defaultdict(TrieNode)

class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert_iterative(self, s:str):
        curr = self.root
        for c in s:
            curr = curr.children[c]
        curr.is_end_of_word = True

    def insert_recursive(self, s, node, i):
        if i == len(s):
            node.is_end_of_word = True
            return
        self.insert_recursive(s, node.children[s[i]], i + 1)

    def search_word_iterative(self, word):
        curr = self.root
        for c in word:
            if c not in curr.children: return False
            curr = curr.children[c]
        return curr.is_end_of_word

    def search_word_recursive(self, word, curr=None, i=0):
        if curr is None: curr = self.root
        if i == len(word):
            return curr.is_end_of_word
        if word[i] not in curr.children:
            return False
        return self.search_word_recursive(word, curr[word[i]], i + 1)

    def delete_word(self, word):
        self.delete_word_recursive(self.root, word, 0)

    def delete_word_recursive(self, node, word, i):
        if i == len(word):
            if len(node.children) > 0:
                node.is_end_of_word = False
            return node.children == 0
        if word[i] not in node.children:
            return False
        should_delete_char = self.delete_word_recursive(node.children[word[i]], word, i+1)
        if should_delete_char:
            del node.children[word[i]]
        return len(node.children) == 0
