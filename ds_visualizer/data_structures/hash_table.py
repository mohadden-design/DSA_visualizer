"""
hash_table.py
-------------
Hash Table - stores keys using a hash function that converts a key
into a bucket index. Collisions (two keys landing on the same index)
are resolved here with separate chaining: each bucket is a small
list that can hold more than one key.
"""


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key):
        index = self._hash(key)
        if key not in self.buckets[index]:
            self.buckets[index].append(key)
        return index

    def search(self, key):
        index = self._hash(key)
        return index, key in self.buckets[index]

    def delete(self, key):
        index = self._hash(key)
        if key in self.buckets[index]:
            self.buckets[index].remove(key)
            return True
        return False

    def reset(self):
        self.buckets = [[] for _ in range(self.size)]
