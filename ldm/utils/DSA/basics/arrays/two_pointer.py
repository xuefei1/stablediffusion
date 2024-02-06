"""
Fast & slow pointers (moving in the same direction)
- Detect cycle in linked list.

Colliding pointers (moving in different directions)
- Sort 3 colors.

LC 15, 18, 42, 457
"""


class ListNode:

    def __init__(self, val):
        self.val = val
        self.next = None


def has_cycle_linked_list(head):
    slow, fast = head, head
    while fast is not None and slow is not None:
        slow = slow.next
        fast = fast.next
        fast = fast.next if fast is not None else None
        if slow == fast and fast is not None:
            return True
    return False


def sort_3_colors(arr):
    """
    Use colliding pointer to sort an array of only 0, 1, 2. Such that all the 0 are grouped before 1 and all the 1 before 2.
    l tracks the next location to put 0.
    r tracks the next location to put 2.
    i tracks the current comparison, only increment i if arr[i] == 1.
    O(n) time O(1) space
    """
    l, i = 0, 0
    r = len(arr) - 1
    while i < r:
        if arr[i] == 0:
            while arr[l] == 0:
                l += 1
            arr[i], arr[l] = arr[l], arr[i]
            l += 1
        elif arr[i] == 2:
            while arr[r] == 2:
                r -= 1
            arr[i], arr[r] = arr[r], arr[i]
            r -= 1
        else:
            i += 1
    return arr


if __name__ == "__main__":
    print(sort_3_colors([1,1,2,0,2,0,0,2,2,1,2,1,2,1,2,1,2,0,0,0,1,2,2,0,2,0,2,0,2]))
