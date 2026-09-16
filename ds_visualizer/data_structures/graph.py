"""
graph.py
--------
Graph - a set of vertices connected by edges, stored here as an
adjacency list. Supports both directed and undirected mode, plus
BFS and DFS traversal.
"""


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adjacency = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []
            return True
        return False

    def add_edge(self, v1, v2):
        self.add_vertex(v1)
        self.add_vertex(v2)
        if v2 not in self.adjacency[v1]:
            self.adjacency[v1].append(v2)
        if not self.directed and v1 not in self.adjacency[v2]:
            self.adjacency[v2].append(v1)

    def delete_vertex(self, vertex):
        if vertex in self.adjacency:
            del self.adjacency[vertex]
            for v in self.adjacency:
                if vertex in self.adjacency[v]:
                    self.adjacency[v].remove(vertex)

    def delete_edge(self, v1, v2):
        if v1 in self.adjacency and v2 in self.adjacency[v1]:
            self.adjacency[v1].remove(v2)
        if not self.directed and v2 in self.adjacency and v1 in self.adjacency[v2]:
            self.adjacency[v2].remove(v1)

    def bfs(self, start):
        if start not in self.adjacency:
            return []
        visited = [start]
        queue = [start]
        order = [start]
        while queue:
            current = queue.pop(0)
            for neighbor in sorted(self.adjacency[current], key=str):
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
                    order.append(neighbor)
        return order

    def dfs(self, start):
        if start not in self.adjacency:
            return []
        visited = []
        def walk(v):
            visited.append(v)
            for neighbor in sorted(self.adjacency[v], key=str):
                if neighbor not in visited:
                    walk(neighbor)
        walk(start)
        return visited

    def reset(self):
        self.adjacency = {}
