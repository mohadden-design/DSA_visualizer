"""
bplus_tree.py
-------------
B+ Tree (simplified, for teaching purposes) - a self-balancing,
multi-way search tree where all keys live in the leaf nodes, and
those leaves are linked together for fast range scans. Internal
nodes only store "signpost" keys used to guide the search down to
the right leaf.
"""


class BPlusNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []   # only used by internal nodes
        self.next = None     # leaf-to-leaf link (leaves only)


class BPlusTree:
    def __init__(self, order=4):
        self.order = order          # max children per internal node
        self.root = BPlusNode(leaf=True)
        self.last_split = False     # so the UI can announce a split happened

    def insert(self, key):
        self.last_split = False
        root = self.root
        if len(root.keys) == self.order - 1:
            new_root = BPlusNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            self.last_split = True
        self._insert_non_full(self.root, key)

    def _split_child(self, parent, index):
        node = parent.children[index]
        mid = len(node.keys) // 2

        if node.leaf:
            new_node = BPlusNode(leaf=True)
            new_node.keys = node.keys[mid:]
            node.keys = node.keys[:mid]
            new_node.next = node.next
            node.next = new_node
            parent.keys.insert(index, new_node.keys[0])
            parent.children.insert(index + 1, new_node)
        else:
            new_node = BPlusNode(leaf=False)
            mid_key = node.keys[mid]
            new_node.keys = node.keys[mid + 1:]
            new_node.children = node.children[mid + 1:]
            node.keys = node.keys[:mid]
            node.children = node.children[:mid + 1]
            parent.keys.insert(index, mid_key)
            parent.children.insert(index + 1, new_node)

    def _insert_non_full(self, node, key):
        if node.leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node.keys.insert(i, key)
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            child = node.children[i]
            if len(child.keys) == self.order - 1:
                self._split_child(node, i)
                self.last_split = True
                if key >= node.keys[i]:
                    i += 1
                child = node.children[i]
            self._insert_non_full(child, key)

    def search(self, key):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        return key in node.keys

    def leaf_traversal(self):
        node = self.root
        while not node.leaf:
            node = node.children[0]
        result = []
        while node:
            result.extend(node.keys)
            node = node.next
        return result

    def reset(self):
        self.root = BPlusNode(leaf=True)
        self.last_split = False
