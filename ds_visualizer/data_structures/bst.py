"""
bst.py
------
Binary Search Tree (BST) - a binary tree where, for every node, all
values in the left subtree are smaller and all values in the right
subtree are larger than the node itself.
"""


class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return BSTNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node

    def search(self, value):
        node = self.root
        while node:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def find_min(self, node="root"):
        node = self.root if node == "root" else node
        if node is None:
            return None
        while node.left:
            node = node.left
        return node.value

    def find_max(self, node="root"):
        node = self.root if node == "root" else node
        if node is None:
            return None
        while node.right:
            node = node.right
        return node.value

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor_value = self.find_min(node.right)
            node.value = successor_value
            node.right = self._delete(node.right, successor_value)
        return node

    def inorder(self):
        result = []
        def walk(n):
            if n:
                walk(n.left); result.append(n.value); walk(n.right)
        walk(self.root)
        return result

    def preorder(self):
        result = []
        def walk(n):
            if n:
                result.append(n.value); walk(n.left); walk(n.right)
        walk(self.root)
        return result

    def postorder(self):
        result = []
        def walk(n):
            if n:
                walk(n.left); walk(n.right); result.append(n.value)
        walk(self.root)
        return result

    def level_order(self):
        result = []
        if self.root is None:
            return result
        queue = [self.root]
        while queue:
            n = queue.pop(0)
            result.append(n.value)
            if n.left:
                queue.append(n.left)
            if n.right:
                queue.append(n.right)
        return result

    def reset(self):
        self.root = None
