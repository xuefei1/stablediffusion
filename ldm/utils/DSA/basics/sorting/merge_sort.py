from type_classes import ListNode

"""
MergeSort O(nlogn) not in place, stable
Array is continuously divided into two sub-arrays, then, 1 element array is sorted by default, and other sub-arrays have their element compared one by one and joined together in order, into 1 array
Mergesort involves two processes, divide and merge
"""
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    first_half, second_half = arr[:mid], arr[mid:]
    left_sorted_arr = merge_sort(first_half)
    right_sorted_arr = merge_sort(second_half)
    return merge(left_sorted_arr, right_sorted_arr)


def merge(arr1, arr2):
    i, j, ans = 0, 0, []
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            ans.append(arr1[i])
            i += 1
        else:
            ans.append(arr2[j])
            j += 1
    ans.extend(arr1[i:] if i < len(arr1) else arr2[j:]) # add any remaining elements
    return ans


"""
Merge sort two linked lists

Runner approach with 3 pointers, to divide the list in half in each recursive call
"""
def merge_sort_linked_lists(head):
    if head is None or head.next is None:
        return head
    # p1 move 1 step every time, p2 move 2 step every time, p1_prev record node before p1, i.e., the end of first half
    p1, p2, p1_prev = head, head, head
    while p2 is not None and p2.next is not None:
        p1_prev = p1
        p1 = p1.next
        p2 = p2.next.next
    # change pre next to None, make two sub-lists (head to pre, p1 to p2)
    p1_prev.next = None
    # recursive divide
    left_sorted_head = merge_sort_linked_lists(head)
    right_sorted_head = merge_sort_linked_lists(p1)
    return merge_lists(left_sorted_head, right_sorted_head)

def merge_lists(h1, h2):
    if h1 is None: return h2
    if h2 is None: return h1
    if h1.val <= h2.val:
        h1.next = merge_lists(h1.next, h2)
        return h1
    else:
        h2.next = merge_lists(h1, h2.next)
        return h2
    
"""
Why is mergeSort sometimes preferred over quickSort?
  
Quick sort works well for sorting in-place. In particular, most of the operations can be defined in terms of swapping pairs of elements in an array. 
To do that, however, you normally "walk" through the array with two pointers (or indexes, etc.) 
One starts at the beginning of the array and the other at the end. Both then work their way toward the middle 
(and you're done with a particular partition step when they meet). That's expensive with files, 
because files are oriented primarily toward reading in one direction, from beginning to end. 
Starting from the end and seeking backwards is usually relatively expensive.
At least in its simplest incarnation, merge sort is pretty much the opposite. 
The easy way to implement it only requires looking through the data in one direction, but involves breaking the data into two separate pieces, 
sorting the pieces, then merging them back together.

You can't index directly into a linked list very quickly. That is, if myList is a linked list, then myList[x], were it possible to write such syntax, 
would involve starting at the head of the list and following the first x links. That would have to be done twice for every comparison that Quicksort makes, 
and that would get expensive real quick. Same thing on disk: Quicksort would have to seek and read every item it wants to compare.

With a linked list, it's easy to take (for example) alternating elements in one linked list, and manipulate the links to create two linked lists from those 
same elements instead. With an array, rearranging elements so alternating elements go into separate arrays is easy if you're willing to create a copy as big as 
the original data, but otherwise rather more non-trivial.

Likewise, merging with arrays is easy if you merge elements from the source arrays into a new array with the data in order -- but to do it in place without 
creating a whole new copy of the data is a whole different story. With a linked list, merging elements together from two source lists into a single target 
list is trivial -- again, you just manipulate links, without copying elements.

Quicksort has better locality of reference than mergesort, (i.e. do we read lots of elements which are probably in cache?) 
which means that the accesses performed in quicksort are usually faster than the corresponding accesses in mergesort.

Quicksort uses worst-case O(log n) memory (if implemented correctly), while mergesort requires O(n) memory due to the overhead of merging.

Merge sort has a guaranteed upper limit of O(N log2N)
Quick sort has a guaranteed upper limit of O(N^2)

Quick sort has low memory requirement, and faster since its inner loop can be implemented nicely on most architectures
"""

if __name__ == "__main__":
    print(merge_sort([1,4,6,2,3,7,9,3,-2,-5,-5,3,2,6,8,4,11]))
