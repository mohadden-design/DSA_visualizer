"""
info.py
-------
Static reference content: a short definition and a complexity table
for every data structure. Kept separate from the UI code so it is
easy to read, edit, or extend without touching app.py.
"""

DS_INFO = {
    "Queue": {
        "definition": (
            "A Queue is a linear data structure that follows the FIFO "
            "(First In, First Out) principle - the first element added is "
            "the first one removed, just like a line of people waiting."
        ),
        "complexity": [
            ("Enqueue", "O(1)", "O(1)"),
            ("Dequeue", "O(1)", "O(1)"),
            ("Peek",    "O(1)", "O(1)"),
            ("Search",  "O(n)", "O(n)"),
        ],
        "space": "O(n)",
    },
    "Stack": {
        "definition": (
            "A Stack is a linear data structure that follows the LIFO "
            "(Last In, First Out) principle - the most recently added "
            "element is the first one removed, like a stack of plates."
        ),
        "complexity": [
            ("Push", "O(1)", "O(1)"),
            ("Pop",  "O(1)", "O(1)"),
            ("Peek", "O(1)", "O(1)"),
            ("Search", "O(n)", "O(n)"),
        ],
        "space": "O(n)",
    },
    "Singly Linked List": {
        "definition": (
            "A Singly Linked List is a sequence of nodes where each node "
            "stores a value and a pointer to the next node. It allows fast "
            "insertion/deletion at the head but only forward traversal."
        ),
        "complexity": [
            ("Insert at beginning", "O(1)", "O(1)"),
            ("Insert at end",       "O(n)", "O(n)"),
            ("Delete",              "O(n)", "O(n)"),
            ("Search",              "O(n)", "O(n)"),
        ],
        "space": "O(n)",
    },
    "Doubly Linked List": {
        "definition": (
            "A Doubly Linked List is like a Singly Linked List, but each "
            "node also stores a pointer to the previous node, allowing "
            "traversal in both directions."
        ),
        "complexity": [
            ("Insert at beginning", "O(1)", "O(1)"),
            ("Insert at end",       "O(1)", "O(1)"),
            ("Delete",              "O(n)", "O(n)"),
            ("Search",              "O(n)", "O(n)"),
        ],
        "space": "O(n)",
    },
    "Tree": {
        "definition": (
            "A (general) Tree is a hierarchical structure made of nodes, "
            "where each node can have any number of children and there is "
            "exactly one path from the root to any other node."
        ),
        "complexity": [
            ("Add node",   "O(n)", "O(n)"),
            ("Delete node", "O(n)", "O(n)"),
            ("Traversal",  "O(n)", "O(n)"),
        ],
        "space": "O(n)",
    },
    "Binary Search Tree": {
        "definition": (
            "A Binary Search Tree (BST) is a binary tree where, for every "
            "node, all values in the left subtree are smaller and all "
            "values in the right subtree are larger than the node itself."
        ),
        "complexity": [
            ("Search", "O(log n)", "O(n)"),
            ("Insert", "O(log n)", "O(n)"),
            ("Delete", "O(log n)", "O(n)"),
        ],
        "space": "O(n)",
    },
    "AVL Tree": {
        "definition": (
            "An AVL Tree is a self-balancing Binary Search Tree in which "
            "the height difference (balance factor) between the left and "
            "right subtrees of any node is at most 1. Rotations keep it "
            "balanced after every insert/delete."
        ),
        "complexity": [
            ("Search", "O(log n)", "O(log n)"),
            ("Insert", "O(log n)", "O(log n)"),
            ("Delete", "O(log n)", "O(log n)"),
        ],
        "space": "O(n)",
    },
    "B+ Tree": {
        "definition": (
            "A B+ Tree is a self-balancing, multi-way search tree where "
            "all actual data (keys) is stored in the leaf nodes, and those "
            "leaves are linked together in a chain for fast range queries. "
            "Internal nodes only store keys used to guide the search. This "
            "makes B+ Trees ideal for database and file-system indexing, "
            "since a shallow tree means very few disk reads are needed to "
            "find any record."
        ),
        "complexity": [
            ("Search", "O(log n)", "O(log n)"),
            ("Insert", "O(log n)", "O(log n)"),
            ("Range/leaf scan", "O(n)", "O(n)"),
        ],
        "space": "O(n)",
    },
    "Graph": {
        "definition": (
            "A Graph is a set of vertices (nodes) connected by edges. It "
            "can be directed or undirected, and is used to model networks "
            "such as maps, social connections, or web links."
        ),
        "complexity": [
            ("Add vertex/edge", "O(1)", "O(1)"),
            ("BFS",  "O(V + E)", "O(V + E)"),
            ("DFS",  "O(V + E)", "O(V + E)"),
        ],
        "space": "O(V + E)",
    },
    "Hash Table": {
        "definition": (
            "A Hash Table stores key-value pairs using a hash function "
            "that converts a key into an index (bucket) in an array. When "
            "two keys hash to the same index (a collision), this app "
            "resolves it using chaining - each bucket holds a small list."
        ),
        "complexity": [
            ("Insert", "O(1)", "O(n)"),
            ("Search", "O(1)", "O(n)"),
            ("Delete", "O(1)", "O(n)"),
        ],
        "space": "O(n)",
    },
}

# Extra teaching notes shown only for structures where the syllabus
# explicitly asks students to "explain" a concept.
HASH_TABLE_NOTES = """
- Hash function: turns a key into a bucket index (here: hash(key) % table_size).
- Collision: two different keys mapping to the same bucket index.
- Collision resolution (this app): separate chaining - each bucket is a
  small list, and colliding keys are simply appended to that list.
- Average-case complexity: O(1) when keys are spread evenly across
  buckets; worst case O(n) if every key collides into one bucket.
"""
