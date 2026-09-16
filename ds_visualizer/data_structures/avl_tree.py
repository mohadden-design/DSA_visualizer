"""
avl_tree.py
-----------
AVL Tree - a self-balancing Binary Search Tree. After every insert
or delete, the tree checks each node's balance factor (height of
left subtree - height of right subtree) and performs a rotation
(LL, RR, LR, or RL) whenever that factor goes outside [-1, 1].
"""


class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self.last_rotation = None  # so the UI can show what just happened

    def _h(self, node):
        return node.height if node else 0

    def balance_factor(self, node):
        return self._h(node.left) - self._h(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self._update_height(x)
        self._update_height(y)
        return y

    def insert(self, value):
        self.last_rotation = None
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node  # no duplicates

        self._update_height(node)
        balance = self.balance_factor(node)

        if balance > 1 and value < node.left.value:          # Left-Left
            self.last_rotation = "LL Rotation (single right rotation)"
            return self._rotate_right(node)
        if balance < -1 and value > node.right.value:        # Right-Right
            self.last_rotation = "RR Rotation (single left rotation)"
            return self._rotate_left(node)
        if balance > 1 and value > node.left.value:           # Left-Right
            self.last_rotation = "LR Rotation (left then right rotation)"
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and value < node.right.value:         # Right-Left
            self.last_rotation = "RL Rotation (right then left rotation)"
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def delete(self, value):
        self.last_rotation = None
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
            successor = node.right
            while successor.left:
                successor = successor.left
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)

        self._update_height(node)
        balance = self.balance_factor(node)

        if balance > 1 and self.balance_factor(node.left) >= 0:
            self.last_rotation = "LL Rotation (single right rotation)"
            return self._rotate_right(node)
        if balance > 1 and self.balance_factor(node.left) < 0:
            self.last_rotation = "LR Rotation (left then right rotation)"
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self.balance_factor(node.right) <= 0:
            self.last_rotation = "RR Rotation (single left rotation)"
            return self._rotate_left(node)
        if balance < -1 and self.balance_factor(node.right) > 0:
            self.last_rotation = "RL Rotation (right then left rotation)"
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def search(self, value):
        node = self.root
        while node:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

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
        self.last_rotation = None
