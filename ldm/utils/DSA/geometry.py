"""
Vector sub: p1[0] - p2[0], p1[1] - p2[1]
Vector add: p1[0] + p2[0], p1[1] + p2[1]
Vector perp: -v[1], v[0]
Euclidean dist: sqrt( (p2[0]-p1[0])**2 + ... )
Vector norm: p[0] / sqrt( p[0]**2 + p[1]**2 ), p1[1] / sqrt( p[0]**2 + p[1]**2 )
Vector cross prod: v1_x * v2_y - v1_y * v2_x
Vector dot prod: v1_x * v2_x + v1_y * v2_y
Vector mid point: (v1_x + v2_x) // 2, (v1_y + v2_y) // 2
Two vectors orientation: ori = (q1-p1)*(r0-q0) - (q0-p0)*(r1-q1)
0: colinear
1: clockwise
2: counter-clockwise
"""


"""
Problem: Determine if two line segments (A,B), (C,D) intersects
A.x, A.y gives the x/y coordinates
These intersect if and only if points A and B are separated by segment CD and points C and D are separated by segment AB. If points A and B are separated by segment CD then ACD and BCD should have opposite orientation meaning either ACD or BCD is counterclockwise but not both. Therefore calculating if two line segments AB and CD intersect is as follows
"""
def ccw(A,B,C):
    return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


"""
Problem: Counting Rectangles in a 2D Grid

Given a list of points in a 2D plane, each point represented as a tuple (x, y), write a Python program to count the number of rectangles that can be formed with sides parallel to the axes. A rectangle is defined by four points that form its vertices, and all sides of the rectangle must be of positive length.

Constraints:
The list of points may contain duplicates, but each point should be considered only once.
All coordinates are integers.
The sides of the rectangles are aligned with the x and y axes (axis-aligned rectangles).

Input: points = [(1, 1), (1, 2), (2, 1), (2, 2)]
Output: 1
Explanation: There is one rectangle formed by the points (1,1), (1,2), (2,1), (2,2).

"""
def count_rectangles(points):
    # Convert list of points to a set for O(1) lookups
    point_set = set(points)
    rectangles = set()
    n = len(points)

    # Iterate over all pairs of points
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]

            # Check if p1 and p2 can be diagonally opposite corners
            if p1[0] != p2[0] and p1[1] != p2[1]:
                # Potential other two corners
                corner1 = (p1[0], p2[1])
                corner2 = (p2[0], p1[1])

                # Check if the other two corners exist
                if corner1 in point_set and corner2 in point_set:
                    # Sort the rectangle's points to ensure uniqueness
                    rectangle = tuple(sorted([p1, p2, corner1, corner2]))
                    rectangles.add(rectangle)

    # The number of unique rectangles
    return len(rectangles)

# Example usage:
points = [(1, 1), (1, 2), (2, 1), (2, 2)]
print(count_rectangles(points))  # Output: 1


"""
How to check if a point (x,y) is on a line segment
"""
def isBetween(a, b, c, epsilon=1e-10):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > epsilon:
        # Cross prod is zero means the shape area spanned by 3 vecs is zero, so they are on the same line
        return False

    # Further check with dot product if point is in line
    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True



"""
Problem: Point-in-Polygon Test Using Ray Casting
Write a Python function to determine whether a given point is inside a simple polygon. The polygon is represented as a list of its vertex coordinates in order (either clockwise or counterclockwise). The point is given as a tuple (x, y). Implement the ray casting algorithm to solve this problem.

Constraints:
The polygon is a simple polygon (non-intersecting edges).
The polygon can be convex or concave.
The point may lie inside, outside, or exactly on the edge of the polygon.
Your function should return True if the point is inside the polygon or on its edge, and False otherwise.
"""
def is_point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]

    for i in range(n + 1):
        p2x, p2y = polygon[i % n]

        # Check if point is on vertex
        if (x, y) == (p1x, p1y):
            return True

        # Check if point is on edge
        # First check if point is within the rectangle bounded by the two edge ends.
        # Compute the slopes of edge vector and point to one of the edge end and check if they are equal.
        minX = min(p1x, p2x)
        maxX = max(p1x, p2x)
        minY = min(p1y, p2y)
        maxY = max(p1y, p2y)
        if minY != maxY: # Edge is not horixontal, otherwise slope is 0
            if (y - p1y) / (x - p1x + 1e-10) == (p2y - p1y) / (p2x - p1x + 1e-10): # Slope equal
                if minX <= x <= maxX and minY <= y <= maxY:
                    return True

        # Check for intersection
        # First check if point is within Y range
        # Then check point is to the right of edge, by checking X values
        # Finally check if point's slope is larger tha edge's slope
        # If all yes, point will intersect with ray case
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y + 1e-10) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

# Example usage:
polygon = [(0,0), (5,0), (5,5), (0,5)]
point_inside = (3, 3)
point_outside = (6, 6)
point_on_edge = (5, 2)

print(is_point_in_polygon(point_inside, polygon))   # Output: True
print(is_point_in_polygon(point_outside, polygon))  # Output: False
print(is_point_in_polygon(point_on_edge, polygon))  # Output: True



"""
Given a list of points in 2D space, write a Python function to find the pair of points that are closest to each other in terms of Euclidean distance. Optimize your solution to have a time complexity better than O(n²).
https://www.youtube.com/watch?v=ldHA8UcQI9Q&ab_channel=Insidecode
"""
import math

def closest_pair_of_points(points):
    # Preprocess: sort the points by x and y coordinates
    Px = sorted(points, key=lambda p: p[0])
    Py = sorted(points, key=lambda p: p[1])

    # Recursive function
    def closest_pair_rec(Px, Py):
        n = len(Px)
        # Base case
        if n <= 3:
            return brute_force_closest_pair(Px)
        # Divide x-ordered parts
        mid = n // 2
        Qx = Px[:mid]
        Rx = Px[mid:]

        # Midpoint x-coordinate
        mid_x = Px[mid][0]

        # Split Py into Qy and Ry
        Qy = []
        Ry = []
        for point in Py:
            if point[0] <= mid_x:
                Qy.append(point)
            else:
                Ry.append(point)

        # Conquer
        (dl, pair_left) = closest_pair_rec(Qx, Qy)
        (dr, pair_right) = closest_pair_rec(Rx, Ry)

        # Find minimal distance
        if dl < dr:
            d = dl
            min_pair = pair_left
        else:
            d = dr
            min_pair = pair_right

        # Merge step
        (d_min_strip, strip_pair) = closest_split_pair(Px, Py, d, min_pair)

        if d_min_strip < d:
            return (d_min_strip, strip_pair)
        else:
            return (d, min_pair)

    # Call the recursive function
    return closest_pair_rec(Px, Py)

def brute_force_closest_pair(P):
    min_dist = math.inf
    min_pair = None
    n = len(P)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = P[i], P[j]
            dist = euclidean_distance(p1, p2)
            if dist < min_dist:
                min_dist = dist
                min_pair = (p1, p2)
    return (min_dist, min_pair)

def closest_split_pair(Px, Py, delta, best_pair):
    # NOTE here Py contains both left and right points before the current split
    n = len(Px)
    mid_x = Px[n // 2][0]
    # Find points within the region of interest
    # Which could potentially give a shorter dist for a point in left with another in right
    Sy = [p for p in Py if abs(p[0] - mid_x) < delta]
    min_dist = delta
    len_Sy = len(Sy)
    min_pair = best_pair
    for i in range(len_Sy):
        # Py is sorted in downward inc fashion, so we only need to check 6 other points below it.
        for j in range(i + 1, min(i + 7, len_Sy)):
            p1, p2 = Sy[i], Sy[j]
            dist = euclidean_distance(p1, p2)
            if dist < min_dist:
                min_dist = dist
                min_pair = (p1, p2)
    return (min_dist, min_pair)

def euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Example usage:
if __name__ == "__main__":
    points = [(2.1, 3.5), (0.4, 1.2), (4.7, 2.2), (3.1, 3.8), (2.9, 2.0), (5.0, 3.0)]
    distance, pair = closest_pair_of_points(points)
    print(f"The closest pair is {pair} with a distance of {distance:.4f}")
