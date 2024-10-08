

def largestRectangleArea(heights) -> int:
    stack = [-1]
    max_area = 0
    for i in range(len(heights)):
        while stack[-1] != -1 and heights[stack[-1]] >= heights[i]:
            current_height = heights[stack.pop()]
            current_width = i - stack[-1] - 1
            a = current_height * current_width
            max_area = max(max_area, a)
        stack.append(i)

    while stack[-1] != -1:
        current_height = heights[stack.pop()]
        current_width = len(heights) - stack[-1] - 1
        max_area = max(max_area, current_height * current_width)
    return max_area


if __name__ == "__main__":
    largestRectangleArea([3,3,3,2,3,3,3,3,3,3,3])