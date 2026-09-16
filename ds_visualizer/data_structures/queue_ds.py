"""
queue_ds.py
-----------
Queue - a linear data structure that follows FIFO (First In, First
Out): the first value added is the first one removed.
(Named queue_ds.py, not queue.py, so it never collides with Python's
own built-in 'queue' module.)
"""


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.pop(0)

    def peek(self):
        return None if self.is_empty() else self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def reset(self):
        self.items = []
