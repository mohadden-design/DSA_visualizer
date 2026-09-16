"""
Quick sanity tests for data_structures.py.
Run with: python3 test_data_structures.py
Not a formal test suite - just enough to catch logic bugs.
"""
from data_structures import (
    Queue, Stack, SinglyLinkedList, DoublyLinkedList, GeneralTree,
    BST, AVLTree, BPlusTree, Graph, HashTable
)


def check(label, condition):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}")
    if not condition:
        raise AssertionError(label)


# ---- Queue ----
q = Queue()
q.enqueue(1); q.enqueue(2); q.enqueue(3)
check("Queue FIFO order", q.items == [1, 2, 3])
check("Queue dequeue returns front", q.dequeue() == 1)
check("Queue peek after dequeue", q.peek() == 2)

# ---- Stack ----
s = Stack()
s.push(1); s.push(2); s.push(3)
check("Stack LIFO order", s.items == [1, 2, 3])
check("Stack pop returns top", s.pop() == 3)
check("Stack peek after pop", s.peek() == 2)

# ---- Singly Linked List ----
sll = SinglyLinkedList()
sll.insert_at_end(1); sll.insert_at_end(2); sll.insert_at_end(3)
sll.insert_at_beginning(0)
sll.insert_at_position(99, 2)
check("SLL order", sll.to_list() == [0, 1, 99, 2, 3])
check("SLL search found", sll.search(99) == 2)
sll.delete(99)
check("SLL delete", sll.to_list() == [0, 1, 2, 3])

# ---- Doubly Linked List ----
dll = DoublyLinkedList()
dll.insert_at_end(1); dll.insert_at_end(2); dll.insert_at_end(3)
check("DLL forward", dll.to_list_forward() == [1, 2, 3])
check("DLL backward", dll.to_list_backward() == [3, 2, 1])
dll.delete(2)
check("DLL delete middle", dll.to_list_forward() == [1, 3])

# ---- General Tree ----
gt = GeneralTree()
gt.add_node(None, "A")
gt.add_node("A", "B")
gt.add_node("A", "C")
gt.add_node("B", "D")
check("Tree preorder", gt.preorder() == ["A", "B", "D", "C"])
check("Tree level order", gt.level_order() == ["A", "B", "C", "D"])

# ---- BST ----
bst = BST()
for v in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(v)
check("BST inorder is sorted", bst.inorder() == sorted([50, 30, 70, 20, 40, 60, 80]))
check("BST search hit", bst.search(60) is True)
check("BST search miss", bst.search(99) is False)
check("BST min/max", bst.find_min() == 20 and bst.find_max() == 80)
bst.delete(30)
check("BST delete node with two children", 30 not in bst.inorder())

# ---- AVL Tree ----
avl = AVLTree()
for v in [10, 20, 30, 40, 50, 25]:  # forces multiple rotation types
    avl.insert(v)
def height(n):
    return 0 if n is None else 1 + max(height(n.left), height(n.right))
h = height(avl.root)
import math
n_nodes = len(avl.inorder())
check("AVL stays balanced (height close to log2(n))", h <= math.ceil(math.log2(n_nodes + 1)) + 1)
check("AVL inorder sorted", avl.inorder() == sorted(avl.inorder()))

# ---- B+ Tree ----
bpt = BPlusTree(order=4)
for v in [10, 20, 5, 6, 12, 30, 7, 17]:
    bpt.insert(v)
check("B+ tree leaf traversal sorted", bpt.leaf_traversal() == sorted([10, 20, 5, 6, 12, 30, 7, 17]))
check("B+ tree search hit", bpt.search(12) is True)
check("B+ tree search miss", bpt.search(999) is False)

# ---- Graph ----
g = Graph()
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")
g.add_edge("C", "D")
check("Graph BFS visits all", set(g.bfs("A")) == {"A", "B", "C", "D"})
check("Graph DFS visits all", set(g.dfs("A")) == {"A", "B", "C", "D"})
g.delete_edge("A", "B")
check("Graph delete edge", "B" not in g.adjacency["A"])

# ---- Hash Table ----
ht = HashTable(size=5)
ht.insert(10); ht.insert(15); ht.insert(20)  # 10 and 15 and 20 all % 5 == 0 -> collision chain
check("Hash table collisions chained in same bucket", len(ht.buckets[0]) == 3)
idx, found = ht.search(15)
check("Hash table search hit", found is True)
ht.delete(15)
check("Hash table delete", 15 not in ht.buckets[0])

print("\nAll data structure logic checks passed.")
