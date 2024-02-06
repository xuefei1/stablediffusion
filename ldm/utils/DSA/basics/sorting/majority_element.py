

"""
Find the number that appears more than half of the len(arr) times.

The majority element must be the median.
The majority element must be the mode.

Find median first, then check if it is majority element.
"""

def maj_element_candidate(arr):
    c = 0
    maj = None
    for v in arr:
        if c == 0:
            maj = v
            c += 1
        else:
            if maj == v:
                c += 1
            else:
                c -= 1
    assert maj is not None
    return maj
