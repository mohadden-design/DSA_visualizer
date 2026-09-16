"""
stack.py
--------
Stack - a linear data structure that follows LIFO (Last In, First
Out): the most recently added value is the first one removed.
"""


class Stack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        return None if self.is_empty() else self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def reset(self):
        self.items = []
