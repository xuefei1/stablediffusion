

"""
1011. Capacity To Ship Packages Within D Days
A conveyor belt has packages that must be shipped from one port to another within D days.

The i-th package on the conveyor belt has a weight of weights[i].
Each day, we load the ship with packages on the conveyor belt (in the order given by weights).
We may not load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within D days.
---
The key is that we do not return once a valid solution is found, instead we keep shrinking upper_bound to find the min
"""
class Solution1011:

    def canShipInDays(self, capacity, weights, n_days):
        curr_n_days = 1
        curr_payload = 0
        for w in weights:
            curr_payload += w
            if curr_payload > capacity:
                curr_n_days += 1
                curr_payload = w
            if curr_n_days > n_days: break
        return curr_n_days <= n_days

    def shipWithinDays(self, weights, D: int) -> int:
        lower_bound = max(weights)
        upper_bound = sum(weights)
        while lower_bound <= upper_bound:
            mid = lower_bound + (upper_bound - lower_bound) // 2
            if not self.canShipInDays(mid, weights, D):
                lower_bound = mid + 1
            else:
                upper_bound = mid -1
        return lower_bound


class Solution973:
    """
    We have a list of points on the plane.  Find the K closest points to the origin (0, 0).
    (Here, the distance between two points on a plane is the Euclidean distance.)
    You may return the answer in any order.  The answer is guaranteed to be unique (except for the order that it is in.)

    Sorting is not necessary because the answer can be in any order
    Max heap solution: keep at most K points in the max heap, pop any large points, in the end, the heap contains K closest points
    Quick select solution: partially quick sort the points, return the first K points
    """
    def kClosest_max_heap(self, points, K: int):
        import heapq
        max_heap = []
        heapq.heapify(max_heap)
        for p in points:
            d = p[0]**2 + p[1]**2
            heapq.heappush(max_heap, (-d, p))
            if len(max_heap) > K:
                heapq.heappop(max_heap)
        return [t[1] for t in max_heap]

    def kClosest_quick_select(self, points, K):
        dist = lambda i: points[i][0] ** 2 + points[i][1] ** 2
        def sort(i, j, K):
            # Partially sorts A[i:j+1] so the first K elements are
            # the smallest K elements.
            if i >= j: return
            # Select the pivot, swap it with the first element
            k = i+(j-i)//2
            points[i], points[k] = points[k], points[i]
            mid = partition(i, j)
            if K < mid - i + 1:
                # need to shrink mid, recurse on left part of the array
                sort(i, mid - 1, K)
            elif K > mid - i + 1:
                # only still need to find the K - (mid-i+1) elements, since already have found mid - i + 1 elements
                sort(mid + 1, j, K - (mid - i + 1))

        def partition(i, j):
            # Partition by pivot A[i], returning an index mid
            # such that A[i] <= A[mid] <= A[j] for i < mid < j.
            oi = i
            pivot = dist(i)
            i += 1 # avoid pivot
            while True:
                while i < j and dist(i) < pivot:
                    i += 1
                while i <= j and dist(j) >= pivot:
                    j -= 1
                if i >= j: break
                points[i], points[j] = points[j], points[i]
            # This swap moves the pivot to the right place, j is pointing to an element smaller than pivot
            points[oi], points[j] = points[j], points[oi]
            return j # pivot is at the right position j

        sort(0, len(points) - 1, K)
        return points[:K]
