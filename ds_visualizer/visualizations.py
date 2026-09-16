"""
visualizations.py
------------------
Turns the *state* of a data structure (a plain list, or a tree of
nodes) into a Plotly Figure. Every function here is a pure function:
give it data, get back a figure - it never touches the data
structures themselves, which keeps this file easy to reason about.
"""
import math
import plotly.graph_objects as go

# Colors used consistently across every visualization
COLOR_DEFAULT = "#4F86C6"      # normal node/box
COLOR_HIGHLIGHT = "#F4A259"    # just inserted / current / searching
COLOR_VISITED = "#8FBF7F"      # visited (BFS/DFS) or found
COLOR_DELETED = "#E76F51"      # about to be / just deleted
COLOR_ROOT = "#6A4C93"         # root of a tree
COLOR_EDGE = "#9AA5B1"
COLOR_TEXT = "#FFFFFF"
BG_COLOR = "rgba(0,0,0,0)"


def _blank_figure(height=380):
    fig = go.Figure()
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor=BG_COLOR,
        paper_bgcolor=BG_COLOR,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
    )
    return fig


def _add_box(fig, x, y, label, color=COLOR_DEFAULT, w=0.8, h=0.8):
    fig.add_shape(
        type="rect",
        x0=x - w / 2, x1=x + w / 2, y0=y - h / 2, y1=y + h / 2,
        line=dict(color="#2B2D42", width=2),
        fillcolor=color,
    )
    fig.add_annotation(
        x=x, y=y, text=str(label), showarrow=False,
        font=dict(color=COLOR_TEXT, size=14, family="Arial Black"),
    )


def _add_arrow(fig, x0, y0, x1, y1, color=COLOR_EDGE, curved=False):
    fig.add_annotation(
        x=x1, y=y1, ax=x0, ay=y0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=2,
        arrowcolor=color,
    )


# ============================================================
# QUEUE / STACK  (simple linear box layouts)
# ============================================================
def viz_queue(items, highlight_index=None):
    fig = _blank_figure()
    if not items:
        fig.add_annotation(x=0, y=0, text="Queue is empty", showarrow=False,
                            font=dict(size=16, color="#888"))
        fig.update_xaxes(range=[-3, 3]); fig.update_yaxes(range=[-2, 2])
        return fig

    for i, val in enumerate(items):
        color = COLOR_HIGHLIGHT if i == highlight_index else COLOR_DEFAULT
        _add_box(fig, i, 0, val, color)
    fig.add_annotation(x=0, y=1, text="FRONT", showarrow=False, font=dict(color="#888", size=12))
    fig.add_annotation(x=len(items) - 1, y=1, text="REAR", showarrow=False, font=dict(color="#888", size=12))
    fig.update_xaxes(range=[-1.5, len(items) + 0.5])
    fig.update_yaxes(range=[-2, 2])
    return fig


def viz_stack(items, highlight_index=None):
    fig = _blank_figure()
    if not items:
        fig.add_annotation(x=0, y=0, text="Stack is empty", showarrow=False,
                            font=dict(size=16, color="#888"))
        fig.update_xaxes(range=[-3, 3]); fig.update_yaxes(range=[-2, 2])
        return fig

    for i, val in enumerate(items):
        color = COLOR_HIGHLIGHT if i == highlight_index else COLOR_DEFAULT
        _add_box(fig, 0, i, val, color)
    fig.add_annotation(x=1.1, y=len(items) - 1, text="<- TOP", showarrow=False,
                        font=dict(color="#888", size=12))
    fig.update_xaxes(range=[-2, 2.5])
    fig.update_yaxes(range=[-1, len(items) + 1])
    return fig


# ============================================================
# LINKED LISTS
# ============================================================
def viz_singly_linked_list(values, highlight_index=None):
    fig = _blank_figure()
    if not values:
        fig.add_annotation(x=0, y=0, text="List is empty (NULL)", showarrow=False,
                            font=dict(size=16, color="#888"))
        fig.update_xaxes(range=[-3, 3]); fig.update_yaxes(range=[-2, 2])
        return fig

    for i, val in enumerate(values):
        color = COLOR_HIGHLIGHT if i == highlight_index else COLOR_DEFAULT
        _add_box(fig, i * 2, 0, val, color)
        if i < len(values) - 1:
            _add_arrow(fig, i * 2 + 0.4, 0, i * 2 + 1.6, 0)
    _add_arrow(fig, (len(values) - 1) * 2 + 0.4, 0, (len(values) - 1) * 2 + 1.4, 0)
    fig.add_annotation(x=(len(values) - 1) * 2 + 1.6, y=0, text="NULL", showarrow=False,
                        font=dict(color="#888", size=13))
    fig.update_xaxes(range=[-1.5, len(values) * 2 + 1])
    fig.update_yaxes(range=[-2, 2])
    return fig


def viz_doubly_linked_list(values, highlight_index=None):
    fig = _blank_figure()
    if not values:
        fig.add_annotation(x=0, y=0, text="List is empty (NULL)", showarrow=False,
                            font=dict(size=16, color="#888"))
        fig.update_xaxes(range=[-3, 3]); fig.update_yaxes(range=[-2, 2])
        return fig

    fig.add_annotation(x=-1.6, y=0, text="NULL", showarrow=False, font=dict(color="#888", size=13))
    for i, val in enumerate(values):
        color = COLOR_HIGHLIGHT if i == highlight_index else COLOR_DEFAULT
        _add_box(fig, i * 2, 0, val, color)
        if i < len(values) - 1:
            _add_arrow(fig, i * 2 + 0.4, 0.15, i * 2 + 1.6, 0.15)
            _add_arrow(fig, i * 2 + 1.6, -0.15, i * 2 + 0.4, -0.15)
    _add_arrow(fig, -1.4, 0, -0.4, 0)
    fig.add_annotation(x=(len(values) - 1) * 2 + 1.6, y=0, text="NULL", showarrow=False,
                        font=dict(color="#888", size=13))
    fig.update_xaxes(range=[-2.5, len(values) * 2 + 1])
    fig.update_yaxes(range=[-2, 2])
    return fig


# ============================================================
# TREES  (General Tree, BST, AVL share this layout engine)
# ============================================================
def _layout_tree(root, get_children):
    """Assigns (x, y) to every node so the tree renders without overlaps.
    Leaves get sequential x positions; a parent is centered above its
    children. y is simply -depth."""
    positions = {}
    counter = [0]

    def assign(node, depth):
        children = get_children(node)
        if not children:
            x = counter[0]
            counter[0] += 1
        else:
            xs = [assign(c, depth + 1) for c in children]
            x = sum(xs) / len(xs)
        positions[id(node)] = (x, -depth)
        return x

    if root is not None:
        assign(root, 0)
    return positions


def _draw_tree(root, get_children, get_label, is_root_special=True, extra_label=None,
               visited_values=None, current_value=None, get_value=None):
    fig = _blank_figure(height=420)
    if root is None:
        fig.add_annotation(x=0, y=0, text="Tree is empty", showarrow=False,
                            font=dict(size=16, color="#888"))
        fig.update_xaxes(range=[-3, 3]); fig.update_yaxes(range=[-2, 2])
        return fig

    get_value = get_value or get_label
    visited_values = visited_values or []
    positions = _layout_tree(root, get_children)

    # edges first (so they sit behind the node boxes)
    def draw_edges(node):
        x0, y0 = positions[id(node)]
        for child in get_children(node):
            x1, y1 = positions[id(child)]
            fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                           line=dict(color=COLOR_EDGE, width=2))
            draw_edges(child)
    draw_edges(root)

    def draw_nodes(node, depth=0):
        x, y = positions[id(node)]
        val = get_value(node)
        if current_value is not None and val == current_value:
            color = COLOR_HIGHLIGHT
        elif val in visited_values:
            color = COLOR_VISITED
        elif is_root_special and node is root:
            color = COLOR_ROOT
        else:
            color = COLOR_DEFAULT
        label = get_label(node)
        _add_box(fig, x, y, label, color, w=0.9, h=0.6)
        if extra_label:
            note = extra_label(node)
            if note:
                fig.add_annotation(x=x, y=y - 0.45, text=note, showarrow=False,
                                    font=dict(color="#888", size=10))
        for child in get_children(node):
            draw_nodes(child, depth + 1)
    draw_nodes(root)

    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    fig.update_xaxes(range=[min(xs) - 1, max(xs) + 1])
    fig.update_yaxes(range=[min(ys) - 1, max(ys) + 1])
    return fig


def viz_general_tree(root, visited_values=None, current_value=None):
    return _draw_tree(root, lambda n: n.children, lambda n: n.value,
                       visited_values=visited_values, current_value=current_value)


def viz_binary_tree(root, show_balance_factor=False, bf_fn=None,
                     visited_values=None, current_value=None):
    def children(n):
        c = []
        if n.left:
            c.append(n.left)
        if n.right:
            c.append(n.right)
        return c

    extra = (lambda n: f"bf={bf_fn(n)}") if (show_balance_factor and bf_fn) else None
    return _draw_tree(root, children, lambda n: n.value, extra_label=extra,
                       visited_values=visited_values, current_value=current_value)


def viz_bplus_tree(root, visited_keys=None, current_key=None):
    def children(n):
        return [] if n.leaf else n.children

    def label(n):
        return ",".join(str(k) for k in n.keys) if n.keys else "-"

    fig = _blank_figure(height=420)
    if root is None:
        fig.add_annotation(x=0, y=0, text="Tree is empty", showarrow=False,
                            font=dict(size=16, color="#888"))
        fig.update_xaxes(range=[-3, 3]); fig.update_yaxes(range=[-2, 2])
        return fig

    visited_keys = visited_keys or []
    positions = _layout_tree(root, children)

    def draw_edges(node):
        x0, y0 = positions[id(node)]
        for child in children(node):
            x1, y1 = positions[id(child)]
            fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                           line=dict(color=COLOR_EDGE, width=2))
            draw_edges(child)
    draw_edges(root)

    def draw_nodes(node):
        x, y = positions[id(node)]
        if node.leaf and current_key is not None and current_key in node.keys:
            color = COLOR_HIGHLIGHT
        elif node.leaf and any(k in visited_keys for k in node.keys):
            color = COLOR_VISITED
        elif node is root:
            color = COLOR_ROOT
        else:
            color = COLOR_DEFAULT
        _add_box(fig, x, y, label(node), color, w=0.9, h=0.6)
        for child in children(node):
            draw_nodes(child)
    draw_nodes(root)

    # extra: show the linked-leaf chain with dashed arrows underneath
    leaves = []
    def collect_leaves(n):
        if n.leaf:
            leaves.append(n)
        else:
            for c in n.children:
                collect_leaves(c)
    collect_leaves(root)

    min_y = min((p[1] for p in positions.values()), default=0)
    leaf_link_y = min_y - 0.8
    for leaf in leaves:
        if leaf.next is not None and id(leaf.next) in positions:
            x0, _ = positions[id(leaf)]
            x1, _ = positions[id(leaf.next)]
            fig.add_shape(type="line", x0=x0, y0=leaf_link_y, x1=x1, y1=leaf_link_y,
                           line=dict(color=COLOR_HIGHLIGHT, width=2, dash="dot"))
    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    fig.update_xaxes(range=[min(xs) - 1, max(xs) + 1])
    if leaves:
        fig.add_annotation(x=positions[id(leaves[0])][0], y=leaf_link_y - 0.3,
                            text="leaf-level chain (for fast range scans)",
                            showarrow=False, font=dict(color="#888", size=10))
        fig.update_yaxes(range=[leaf_link_y - 1, max(ys) + 1])
    else:
        fig.update_yaxes(range=[min(ys) - 1, max(ys) + 1])
    return fig


# ============================================================
# GRAPH
# ============================================================
def viz_graph(adjacency, visited_order=None, current=None):
    fig = _blank_figure(height=420)
    vertices = list(adjacency.keys())
    if not vertices:
        fig.add_annotation(x=0, y=0, text="Graph is empty", showarrow=False,
                            font=dict(size=16, color="#888"))
        fig.update_xaxes(range=[-3, 3]); fig.update_yaxes(range=[-2, 2])
        return fig

    visited_order = visited_order or []
    n = len(vertices)
    radius = max(1.5, n * 0.5)
    positions = {}
    for i, v in enumerate(vertices):
        angle = 2 * math.pi * i / n
        positions[v] = (radius * math.cos(angle), radius * math.sin(angle))

    drawn_edges = set()
    for v, neighbors in adjacency.items():
        for u in neighbors:
            key = tuple(sorted([str(v), str(u)]))
            if key in drawn_edges:
                continue
            drawn_edges.add(key)
            x0, y0 = positions[v]
            x1, y1 = positions[u]
            edge_color = COLOR_VISITED if (v in visited_order and u in visited_order) else COLOR_EDGE
            fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                           line=dict(color=edge_color, width=2))

    for v in vertices:
        x, y = positions[v]
        if v == current:
            color = COLOR_HIGHLIGHT
        elif v in visited_order:
            color = COLOR_VISITED
        else:
            color = COLOR_DEFAULT
        _add_box(fig, x, y, v, color, w=0.7, h=0.7)

    fig.update_xaxes(range=[-radius - 1.5, radius + 1.5])
    fig.update_yaxes(range=[-radius - 1.5, radius + 1.5])
    return fig


# ============================================================
# HASH TABLE
# ============================================================
def viz_hash_table(buckets, highlight_index=None):
    indices = [str(i) for i in range(len(buckets))]
    contents = []
    for i, bucket in enumerate(buckets):
        contents.append(" -> ".join(str(x) for x in bucket) if bucket else "-")

    fill_colors = []
    for i in range(len(buckets)):
        fill_colors.append(COLOR_HIGHLIGHT if i == highlight_index else "#2B2D42")

    fig = go.Figure(data=[go.Table(
        columnwidth=[60, 300],
        header=dict(values=["Index", "Value(s)"],
                    fill_color="#1F2233", font=dict(color="white", size=13),
                    align="left", height=32),
        cells=dict(values=[indices, contents],
                   fill_color=[["#1F2233"] * len(buckets), fill_colors],
                   font=dict(color="white", size=13),
                   align="left", height=30),
    )])
    fig.update_layout(height=min(420, 60 + 34 * len(buckets)),
                       margin=dict(l=10, r=10, t=10, b=10),
                       paper_bgcolor=BG_COLOR)
    return fig
