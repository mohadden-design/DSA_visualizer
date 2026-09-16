"""
singly_linked_list.py
----------------------
Singly Linked List - a chain of nodes where each node points only to
the next one: Node -> Node -> Node -> NULL.
"""


class SNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, value):
        node = SNode(value)
        node.next = self.head
        self.head = node

    def insert_at_end(self, value):
        node = SNode(value)
        if self.head is None:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def insert_at_position(self, value, position):
        if position <= 0 or self.head is None:
            self.insert_at_beginning(value)
            return
        cur = self.head
        count = 0
        while cur.next and count < position - 1:
            cur = cur.next
            count += 1
        node = SNode(value)
        node.next = cur.next
        cur.next = node

    def delete(self, value):
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            return True
        cur = self.head
        while cur.next:
            if cur.next.value == value:
                cur.next = cur.next.next
                return True
            cur = cur.next
        return False

    def search(self, value):
        cur, index = self.head, 0
        while cur:
            if cur.value == value:
                return index
            cur, index = cur.next, index + 1
        return -1

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.value)
            cur = cur.next
        return result

    def reset(self):
        self.head = None
