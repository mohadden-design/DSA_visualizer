"""
doubly_linked_list.py
-----------------------
Doubly Linked List - like a Singly Linked List, but every node also
points back to the previous node, so it can be walked in both
directions: NULL <- Node <-> Node <-> Node -> NULL.
"""


class DNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_beginning(self, value):
        node = DNode(value)
        if self.head is None:
            self.head = self.tail = node
            return
        node.next = self.head
        self.head.prev = node
        self.head = node

    def insert_at_end(self, value):
        node = DNode(value)
        if self.head is None:
            self.head = self.tail = node
            return
        node.prev = self.tail
        self.tail.next = node
        self.tail = node

    def delete(self, value):
        cur = self.head
        while cur:
            if cur.value == value:
                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev
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

    def to_list_forward(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.value)
            cur = cur.next
        return result

    def to_list_backward(self):
        result, cur = [], self.tail
        while cur:
            result.append(cur.value)
            cur = cur.prev
        return result

    def reset(self):
        self.head = self.tail = None
