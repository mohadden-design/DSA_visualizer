"""
tree.py
-------
General Tree - a hierarchical structure where every node can have any
number of children, and there is exactly one path from the root to
any other node.
"""


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []


class GeneralTree:
    def __init__(self):
        self.root = None

    def add_node(self, parent_value, value):
        new_node = TreeNode(value)
        if self.root is None:
            self.root = new_node
            return True
        parent = self._find(self.root, parent_value)
        if parent:
            parent.children.append(new_node)
            return True
        return False

    def _find(self, node, value):
        if node.value == value:
            return node
        for child in node.children:
            found = self._find(child, value)
            if found:
                return found
        return None

    def delete_node(self, value):
        if self.root is None:
            return False
        if self.root.value == value:
            self.root = None
            return True
        return self._delete(self.root, value)

    def _delete(self, node, value):
        for child in node.children:
            if child.value == value:
                node.children.remove(child)
                return True
            if self._delete(child, value):
                return True
        return False

    def preorder(self):
        result = []
        def walk(n):
            if n is None:
                return
            result.append(n.value)
            for c in n.children:
                walk(c)
        walk(self.root)
        return result

    def postorder(self):
        result = []
        def walk(n):
            if n is None:
                return
            for c in n.children:
                walk(c)
            result.append(n.value)
        walk(self.root)
        return result

    def inorder(self):
        # Convention for a general tree: first child, then root, then the rest
        result = []
        def walk(n):
            if n is None:
                return
            if n.children:
                walk(n.children[0])
            result.append(n.value)
            for c in n.children[1:]:
                walk(c)
        walk(self.root)
        return result

    def level_order(self):
        result = []
        if self.root is None:
            return result
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            queue.extend(node.children)
        return result

    def reset(self):
        self.root = None
