from type_classes import BinTreeNode
"""
A perfect binary tree contains 2d-1 nodes, d is the depth of the tree

"""

def in_order_traversal(node):
    if node is None: return
    in_order_traversal(node.left)
    print(node.val)
    in_order_traversal(node.right)


def in_order_traversal_iterative(root):
    stack = []
    curr = root
    while curr is not None:
        stack.append(curr)
        curr = curr.left
    while len(stack) > 0:
        node = stack.pop()
        print(node.val)
        curr = node.right
        while curr is not None:
            stack.append(curr)
            curr = curr.left


def pre_order_traversal_iterative(root):
    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        print(node.val)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)


"""
Morris in order traversal

In order traversal with constant space

algorithm:
current = root
while current != null:
    if current has no left sub-tree :
            visit(current)
            current = current.right
    else:
            find in order predecessor(right most node in left sub tree), it can be either null or node
                if predecessor.right == null:
                        predecessor.right = current (set a path back to current)
                        current = current.left
                else if predecessor.right = current:
                        predecessor.right = null
                        visit(current) // we can visit current cause left subtree is done
                    current = current.right
"""
def morris_in_order_traversal(root):
    curr = root
    while curr is not None:
        if curr.left is None: # if no left child, visit current node and go right
            print(curr.val)
            curr = curr.right
        else:
            # find in-order predecessor
            pred = curr.left
            # keep going right till the right node is None or the right node is the current node, i.e., a previously set path back to current
            while pred.right is not None and pred.right != curr:
                pred = pred.right

            # if the right node is None, meaning this is the first time visiting, set a path back to current
            if pred.right is None:
                pred.right = curr
                curr = curr.left # after path back to curr is set, we are safe to visit the left sub-tree
            else: # left sub-tree is already visited. Go right after visiting the current node
                pred.right = None
                print(curr.val)
                curr = curr.right


def morris_pre_order_traversal(root):
    curr = root
    while curr is not None:
        if curr.left is None:
            print(curr.val)
            curr = curr.right
        else:
            pred = curr.left
            while pred.right is not None and pred.right != curr:
                pred = pred.right
            if pred.right is None:
                pred.right = curr
                print(curr.val)
                curr = curr.left
            else:
                pred.right = None
                curr = curr.right
