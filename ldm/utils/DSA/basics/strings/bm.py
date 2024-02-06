import collections


"""
BM algorithm
Match from end of pattern to the front.
When mismatch is encountered, shift pattern right, such that the char in pattern that matches the given target are aligned.
If no matching char in pattern, shift entire pattern to the right of mismatched char.
Repeat again from end of pattern to front.
"""


def build_bc_table(p):
    bc = collections.defaultdict(lambda:-1)
    for i, c in enumerate(p):
        bc[c] = i
    return bc



