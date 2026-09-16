"""
data_structures/__init__.py
----------------------------
Each data structure now lives in its own file (queue_ds.py, stack.py,
singly_linked_list.py, ...). This file just re-exports every class
from one place, so the rest of the app can still write:

    from data_structures import Queue, Stack, BST, ...

without caring which individual file a class lives in.
"""
from .queue_ds import Queue
from .stack import Stack
from .singly_linked_list import SNode, SinglyLinkedList
from .doubly_linked_list import DNode, DoublyLinkedList
from .tree import TreeNode, GeneralTree
from .bst import BSTNode, BST
from .avl_tree import AVLNode, AVLTree
from .bplus_tree import BPlusNode, BPlusTree
from .graph import Graph
from .hash_table import HashTable

__all__ = [
    "Queue", "Stack",
    "SNode", "SinglyLinkedList",
    "DNode", "DoublyLinkedList",
    "TreeNode", "GeneralTree",
    "BSTNode", "BST",
    "AVLNode", "AVLTree",
    "BPlusNode", "BPlusTree",
    "Graph",
    "HashTable",
]
