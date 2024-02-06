class FreqStack:

    def __init__(self):
        self.item2bucket = {}
        self.bucket_1 = LinkedBucket(1)
        self.curr_bucket = self.bucket_1

    def push(self, x: int) -> None:
        if x in self.item2bucket:
            bucket = self.item2bucket[x]
            prev_freq = bucket.freq

            if bucket.next_b is None:
                new_bucket = LinkedBucket(prev_freq + 1, bucket, bucket.next_b)
                bucket.next_b = new_bucket
            else:
                new_bucket = bucket.next_b

            new_bucket.push(x)
            self.item2bucket[x] = new_bucket
            if self.curr_bucket == bucket:
                self.curr_bucket = new_bucket
        else:
            self.bucket_1.push(x)
            self.item2bucket[x] = self.bucket_1

    def pop(self) -> int:
        target_bucket = self.curr_bucket
        rv = target_bucket.pop()
        if target_bucket == self.bucket_1:
            del self.item2bucket[rv]
        else:
            self.item2bucket[rv] = target_bucket.prev_b

            if target_bucket.is_empty():
                self.curr_bucket = target_bucket.prev_b

        return rv


# Your FreqStack object will be instantiated and called as such:
# obj = FreqStack()
# obj.push(x)
# param_2 = obj.pop()

class LinkedBucket:

    def __init__(self, freq, prev_b=None, next_b=None):
        self.freq = freq
        self.prev_b = prev_b
        self.next_b = next_b
        self.items = []

    def push(self, item):
        self.items.append(item)

    def is_empty(self):
        return len(self.items) == 0

    def pop(self):
        rv = self.items[-1]
        del self.items[-1]
        return rv


class Skiplist:

    def __init__(self):
        self.head = SkiplistNode("head", None)
        self.max_lvl = 5

    def __str__(self):
        rs = ""
        for lvl in range(len(self.head.lvl2next)):
            n = self.head
            strs = []
            while n is not None:
                strs.append("(v:{},c:{})".format(n.val, n.count))
                n = n.lvl2next[lvl]
            rs += "level {}: ".format(lvl) + "->".join(strs) + "\n"
        return rs

    def __repr__(self):
        return str(self)

    def search(self, target: int) -> bool:
        lvl, node, _ = self.search_last_smaller_node(target, allow_early_termination=True)
        target_node = node.lvl2next[lvl]
        return target_node is not None and target_node.val == target

    def search_last_smaller_node(self, num, allow_early_termination=False):
        curr_node, curr_level = self.head, len(self.head.lvl2next) - 1
        passed_lvl2nodes = {}
        done = False
        while not done:
            while curr_node.lvl2next[curr_level] is not None and curr_node.lvl2next[curr_level].val < num:
                curr_node = curr_node.lvl2next[curr_level]
            passed_lvl2nodes[curr_level] = curr_node
            if allow_early_termination and curr_node.lvl2next[curr_level] is not None and curr_node.lvl2next[curr_level].val == num:
                return curr_level, curr_node, passed_lvl2nodes
            if curr_level > 0:
                curr_level -= 1
                continue
            done = True
        return curr_level, curr_node, passed_lvl2nodes

    def add(self, num: int) -> None:
        lvl, smaller_node, passed_lvl2nodes = self.search_last_smaller_node(num, allow_early_termination=True)
        leq_node = smaller_node.lvl2next[lvl]
        if leq_node is not None and leq_node.val == num:
            leq_node.count += 1
        else:
            new_node = SkiplistNode(num, smaller_node.lvl2next[0])
            smaller_node.lvl2next[0] = new_node
            self.promote(new_node, passed_lvl2nodes)

    def promote(self, node, passed_lvl2nodes):
        import random
        curr_lvl = 1
        while True:
            if curr_lvl == self.max_lvl: break
            if random.random() < 0.5: break
            if curr_lvl in passed_lvl2nodes:
                n = passed_lvl2nodes[curr_lvl]
                node.lvl2next[curr_lvl] = n.lvl2next[curr_lvl]
                n.lvl2next[curr_lvl] = node
            else:
                node.lvl2next[curr_lvl] = self.head.lvl2next[curr_lvl] if curr_lvl in self.head.lvl2next else None
                self.head.lvl2next[curr_lvl] = node
            curr_lvl += 1

    def erase(self, num: int) -> bool:
        _, prev_node, passed_lvl2nodes = self.search_last_smaller_node(num)
        target_node = prev_node.lvl2next[0]
        if target_node is None or target_node.val != num: return False
        target_node.count -= 1
        if target_node.count == 0:
            for lvl, n in passed_lvl2nodes.items():
                if n.lvl2next[lvl] is target_node:
                    n.lvl2next[lvl] = target_node.lvl2next[lvl]
        return True


class SkiplistNode:

    def __init__(self, val, next):
        self.val = val
        self.count = 1
        self.lvl2next = {0: next}

    def __str__(self):
        return "(v:{},c:{})".format(self.val, self.count)

    def __repr__(self):
        return str(self)

