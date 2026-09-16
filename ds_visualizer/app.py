"""
app.py
------
The Dash web application. This file is only responsible for the UI:
building the layout and wiring up one callback. All data structure
logic lives in data_structures.py, all drawing logic lives in
visualizations.py, and all definitions/complexity text lives in
info.py - so this file mostly just calls into those three.

NOTE ON STATE: to keep the code simple and readable for a course
project, each data structure is kept as a single global Python object
on the server (see STATE below). That is perfectly fine for a demo /
single-user deployment. A production multi-user app would instead
keep this state per-user-session (e.g. in a server-side cache keyed
by a session id) instead of a plain global dictionary.

Run locally with:  python app.py
"""
import random

import dash
from dash import Dash, dcc, html, Input, Output, State, ctx

from data_structures import (
    Queue, Stack, SinglyLinkedList, DoublyLinkedList, GeneralTree,
    BST, AVLTree, BPlusTree, Graph, HashTable,
)
from visualizations import (
    viz_queue, viz_stack, viz_singly_linked_list, viz_doubly_linked_list,
    viz_general_tree, viz_binary_tree, viz_bplus_tree, viz_graph, viz_hash_table,
)
from info import DS_INFO, HASH_TABLE_NOTES


# ============================================================
# GLOBAL STATE - one live instance of every data structure
# ============================================================
STATE = {
    "Queue": Queue(),
    "Stack": Stack(),
    "Singly Linked List": SinglyLinkedList(),
    "Doubly Linked List": DoublyLinkedList(),
    "Tree": GeneralTree(),
    "Binary Search Tree": BST(),
    "AVL Tree": AVLTree(),
    "B+ Tree": BPlusTree(),
    "Graph": Graph(),
    "Hash Table": HashTable(),
}
DS_NAMES = list(STATE.keys())
MAX_HISTORY = 12
HIDDEN = {"display": "none"}
SHOWN = {"display": "inline-block"}


# ============================================================
# PER-DS UI CONFIGURATION
# Every entry describes which controls to show for that structure,
# what to label them, and what each input field means.
# ============================================================
DS_CONTROLS = {
    "Queue": dict(
        input1_placeholder="Value to enqueue", show_input2=False, input2_placeholder="",
        op1="Enqueue", op2=None, op3=None, delete="Dequeue", delete2=None,
        search=None, minmax=False, peek="Peek (Front)", random="Generate Random Queue",
        traversal_options=None, graph_mode=False,
    ),
    "Stack": dict(
        input1_placeholder="Value to push", show_input2=False, input2_placeholder="",
        op1="Push", op2=None, op3=None, delete="Pop", delete2=None,
        search=None, minmax=False, peek="Peek (Top)", random="Generate Random Stack",
        traversal_options=None, graph_mode=False,
    ),
    "Singly Linked List": dict(
        input1_placeholder="Value", show_input2=True, input2_placeholder="Position (for Insert at Position)",
        op1="Insert at Beginning", op2="Insert at End", op3="Insert at Position",
        delete="Delete Value", delete2=None,
        search="Search", minmax=False, peek=None, random="Generate Random List",
        traversal_options=["Forward Traversal"], graph_mode=False,
    ),
    "Doubly Linked List": dict(
        input1_placeholder="Value", show_input2=False, input2_placeholder="",
        op1="Insert at Beginning", op2="Insert at End", op3=None,
        delete="Delete Value", delete2=None,
        search="Search", minmax=False, peek=None, random="Generate Random List",
        traversal_options=["Forward Traversal", "Backward Traversal"], graph_mode=False,
    ),
    "Tree": dict(
        input1_placeholder="New node value", show_input2=True,
        input2_placeholder="Parent value (leave empty for root)",
        op1="Add Node", op2=None, op3=None, delete="Delete Node", delete2=None,
        search=None, minmax=False, peek=None, random="Generate Random Tree",
        traversal_options=["Preorder", "Inorder", "Postorder", "Level Order"], graph_mode=False,
    ),
    "Binary Search Tree": dict(
        input1_placeholder="Value", show_input2=False, input2_placeholder="",
        op1="Insert", op2=None, op3=None, delete="Delete", delete2=None,
        search="Search", minmax=True, peek=None, random="Generate Random BST",
        traversal_options=["Preorder", "Inorder", "Postorder", "Level Order"], graph_mode=False,
    ),
    "AVL Tree": dict(
        input1_placeholder="Value", show_input2=False, input2_placeholder="",
        op1="Insert", op2=None, op3=None, delete="Delete", delete2=None,
        search="Search", minmax=False, peek=None, random="Generate Random AVL Tree",
        traversal_options=["Preorder", "Inorder", "Postorder", "Level Order"], graph_mode=False,
    ),
    "B+ Tree": dict(
        input1_placeholder="Key", show_input2=False, input2_placeholder="",
        op1="Insert", op2=None, op3=None, delete=None, delete2=None,
        search="Search", minmax=False, peek=None, random="Generate Random B+ Tree",
        traversal_options=["Leaf-level Traversal"], graph_mode=False,
    ),
    "Graph": dict(
        input1_placeholder="Vertex (e.g. A)", show_input2=True,
        input2_placeholder="Second vertex (for an edge)",
        op1="Add Vertex", op2="Add Edge", op3=None,
        delete="Delete Vertex", delete2="Delete Edge",
        search=None, minmax=False, peek=None, random="Generate Random Graph",
        traversal_options=["BFS from Vertex 1", "DFS from Vertex 1"], graph_mode=True,
    ),
    "Hash Table": dict(
        input1_placeholder="Key (a number works best)", show_input2=False, input2_placeholder="",
        op1="Insert", op2=None, op3=None, delete="Delete", delete2=None,
        search="Search", minmax=False, peek=None, random="Generate Random Keys",
        traversal_options=None, graph_mode=False,
    ),
}


def parse_value(raw):
    """Turn user text into an int when possible, otherwise keep it as
    a (trimmed) string - this lets numeric structures work naturally
    while still allowing graph vertex names like 'A' or 'B'."""
    if raw is None:
        return None
    raw = str(raw).strip()
    if raw == "":
        return None
    try:
        return int(raw)
    except ValueError:
        return raw


# ============================================================
# APP + LAYOUT
# ============================================================
app = Dash(__name__)
app.title = "Data Structures Visualizer"
server = app.server  # needed by most deployment platforms (Render, Railway, ...)


def complexity_table(ds_name):
    rows = DS_INFO[ds_name]["complexity"]
    header = html.Tr([html.Th("Operation"), html.Th("Average"), html.Th("Worst")])
    body = [html.Tr([html.Td(op), html.Td(avg), html.Td(worst)]) for op, avg, worst in rows]
    return html.Table([header] + body, className="complexity-table")


app.layout = html.Div(className="page", children=[

    html.Div(className="header", children=[
        html.H1("Data Structures Visualizer"),
        html.P("Select a data structure, perform operations, and watch it happen live."),
    ]),

    html.Div(className="top-row", children=[
        html.Div(className="selector-block", children=[
            html.Label("Select Data Structure"),
            dcc.Dropdown(
                id="ds-selector",
                options=[{"label": n, "value": n} for n in DS_NAMES],
                value="Queue", clearable=False,
            ),
        ]),
    ]),

    html.Div(id="definition-card", className="definition-card"),

    html.Div(className="main-grid", children=[

        # ---------------- LEFT: controls + visualization ----------------
        html.Div(className="left-panel", children=[

            html.Div(className="controls-card", children=[
                html.H3("Operations"),

                html.Div(className="controls-row", children=[
                    dcc.Input(id="input-value1", type="text", placeholder="Value", debounce=False),
                    dcc.Input(id="input-value2", type="text", placeholder="", style=HIDDEN),
                ]),

                dcc.RadioItems(
                    id="graph-mode-radio",
                    options=[{"label": " Undirected", "value": "undirected"},
                             {"label": " Directed", "value": "directed"}],
                    value="undirected", style=HIDDEN, className="radio-row",
                ),

                html.Div(className="controls-row", children=[
                    html.Button("Insert", id="btn-op1", n_clicks=0, className="btn btn-primary"),
                    html.Button("Op2", id="btn-op2", n_clicks=0, className="btn btn-primary", style=HIDDEN),
                    html.Button("Op3", id="btn-op3", n_clicks=0, className="btn btn-primary", style=HIDDEN),
                    html.Button("Delete", id="btn-delete", n_clicks=0, className="btn btn-danger", style=HIDDEN),
                    html.Button("Delete2", id="btn-delete2", n_clicks=0, className="btn btn-danger", style=HIDDEN),
                    html.Button("Search", id="btn-search", n_clicks=0, className="btn btn-info", style=HIDDEN),
                    html.Button("Peek", id="btn-peek", n_clicks=0, className="btn btn-info", style=HIDDEN),
                    html.Button("Find Min", id="btn-min", n_clicks=0, className="btn btn-info", style=HIDDEN),
                    html.Button("Find Max", id="btn-max", n_clicks=0, className="btn btn-info", style=HIDDEN),
                ]),

                html.Div(className="controls-row", children=[
                    html.Button("Generate Random Data", id="btn-random", n_clicks=0, className="btn btn-secondary"),
                    html.Button("Reset", id="btn-reset", n_clicks=0, className="btn btn-reset"),
                ]),

                html.Div(id="traversal-row", className="controls-row", style=HIDDEN, children=[
                    dcc.Dropdown(id="traversal-select", options=[], value=None, clearable=False,
                                 style={"width": "220px", "display": "inline-block"}),
                    html.Button("Run Traversal", id="btn-traverse", n_clicks=0, className="btn btn-primary"),
                ]),

                html.Div(id="step-slider-container", style=HIDDEN, children=[
                    html.Label("Step through the traversal:"),
                    dcc.Slider(id="step-slider", min=0, max=0, step=1, value=0),
                ]),

                html.Div(id="traversal-order-display", className="traversal-order"),
                html.Div(id="status-message", className="status-message"),
            ]),

            html.Div(className="viz-card", children=[
                html.H3("Visualization"),
                dcc.Graph(id="visualization", config={"displayModeBar": False}),
            ]),
        ]),

        # ---------------- RIGHT: complexity + history ----------------
        html.Div(className="right-panel", children=[
            html.Div(className="info-card", children=[
                html.H3("Operation Complexity"),
                html.Div(id="complexity-table-container"),
                html.Div(id="space-complexity"),
            ]),
            html.Div(className="info-card", children=[
                html.H3("Operation History"),
                html.Div(id="history-log", className="history-log"),
            ]),
        ]),
    ]),

    dcc.Store(id="traversal-order-store", data=[]),
    dcc.Store(id="history-store", data=[]),
])


# ============================================================
# RENDERING HELPERS
# ============================================================
def render_figure(ds_name, visited_values=None, current_value=None, highlight_index=None):
    obj = STATE[ds_name]

    if ds_name == "Queue":
        return viz_queue(obj.items, highlight_index=highlight_index)
    if ds_name == "Stack":
        return viz_stack(obj.items, highlight_index=highlight_index)
    if ds_name == "Singly Linked List":
        return viz_singly_linked_list(obj.to_list(), highlight_index=highlight_index)
    if ds_name == "Doubly Linked List":
        return viz_doubly_linked_list(obj.to_list_forward(), highlight_index=highlight_index)
    if ds_name == "Tree":
        return viz_general_tree(obj.root, visited_values=visited_values, current_value=current_value)
    if ds_name == "Binary Search Tree":
        return viz_binary_tree(obj.root, visited_values=visited_values, current_value=current_value)
    if ds_name == "AVL Tree":
        return viz_binary_tree(obj.root, show_balance_factor=True, bf_fn=obj.balance_factor,
                                visited_values=visited_values, current_value=current_value)
    if ds_name == "B+ Tree":
        return viz_bplus_tree(obj.root, visited_keys=visited_values, current_key=current_value)
    if ds_name == "Graph":
        return viz_graph(obj.adjacency, visited_order=visited_values, current=current_value)
    if ds_name == "Hash Table":
        return viz_hash_table(obj.buckets, highlight_index=highlight_index)
    return viz_queue([])  # fallback, should not happen


def traversal_order(ds_name, traversal_choice, start_vertex=None):
    obj = STATE[ds_name]
    if ds_name == "Singly Linked List":
        return obj.to_list()
    if ds_name == "Doubly Linked List":
        return obj.to_list_backward() if traversal_choice == "Backward Traversal" else obj.to_list_forward()
    if ds_name in ("Tree", "Binary Search Tree", "AVL Tree"):
        mapping = {
            "Preorder": obj.preorder, "Inorder": getattr(obj, "inorder", None),
            "Postorder": obj.postorder, "Level Order": obj.level_order,
        }
        fn = mapping.get(traversal_choice)
        return fn() if fn else []
    if ds_name == "B+ Tree":
        return obj.leaf_traversal()
    if ds_name == "Graph":
        if start_vertex is None or start_vertex not in obj.adjacency:
            return []
        return obj.bfs(start_vertex) if traversal_choice.startswith("BFS") else obj.dfs(start_vertex)
    return []


def push_history(history, ds_name, message):
    entry = f"[{ds_name}] {message}"
    history = [entry] + (history or [])
    return history[:MAX_HISTORY]


def render_history(history):
    if not history:
        return html.P("No operations yet.", className="history-empty")
    return html.Ul([html.Li(h) for h in history])


def generate_random(ds_name):
    obj = STATE[ds_name]
    if ds_name == "Queue":
        for _ in range(5):
            obj.enqueue(random.randint(1, 99))
    elif ds_name == "Stack":
        for _ in range(5):
            obj.push(random.randint(1, 99))
    elif ds_name == "Singly Linked List":
        for _ in range(5):
            obj.insert_at_end(random.randint(1, 99))
    elif ds_name == "Doubly Linked List":
        for _ in range(5):
            obj.insert_at_end(random.randint(1, 99))
    elif ds_name == "Tree":
        values = random.sample(range(1, 99), 6)
        obj.add_node(None, values[0])
        for v in values[1:]:
            parent = random.choice(obj.preorder())
            obj.add_node(parent, v)
    elif ds_name in ("Binary Search Tree", "AVL Tree"):
        for v in random.sample(range(1, 99), 7):
            obj.insert(v)
    elif ds_name == "B+ Tree":
        for v in random.sample(range(1, 99), 8):
            obj.insert(v)
    elif ds_name == "Graph":
        for a, b in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]:
            obj.add_edge(a, b)
    elif ds_name == "Hash Table":
        for _ in range(6):
            obj.insert(random.randint(1, 50))
    return "Random data generated."


def run_operation(trigger, ds_name, obj, v1, v2):
    """Dispatches one button click to the right method on the current
    data structure. Returns (status_message, highlight_index, highlight_value)."""

    # ---------------- Queue ----------------
    if ds_name == "Queue":
        if trigger == "btn-op1":
            obj.enqueue(v1)
            return f"Enqueued {v1}", len(obj.items) - 1, None
        if trigger == "btn-delete":
            val = obj.dequeue()
            return (f"Dequeued {val}" if val is not None else "Queue is empty"), None, None
        if trigger == "btn-peek":
            val = obj.peek()
            return (f"Front is {val}" if val is not None else "Queue is empty"), 0, None

    # ---------------- Stack ----------------
    if ds_name == "Stack":
        if trigger == "btn-op1":
            obj.push(v1)
            return f"Pushed {v1}", len(obj.items) - 1, None
        if trigger == "btn-delete":
            val = obj.pop()
            return (f"Popped {val}" if val is not None else "Stack is empty"), None, None
        if trigger == "btn-peek":
            val = obj.peek()
            top_index = len(obj.items) - 1 if obj.items else None
            return (f"Top is {val}" if val is not None else "Stack is empty"), top_index, None

    # ---------------- Singly Linked List ----------------
    if ds_name == "Singly Linked List":
        if trigger == "btn-op1":
            obj.insert_at_beginning(v1)
            return f"Inserted {v1} at beginning", 0, None
        if trigger == "btn-op2":
            obj.insert_at_end(v1)
            return f"Inserted {v1} at end", len(obj.to_list()) - 1, None
        if trigger == "btn-op3":
            pos = v2 if isinstance(v2, int) else 0
            obj.insert_at_position(v1, pos)
            return f"Inserted {v1} at position {pos}", pos, None
        if trigger == "btn-delete":
            ok = obj.delete(v1)
            return (f"Deleted {v1}" if ok else f"{v1} not found"), None, None
        if trigger == "btn-search":
            idx = obj.search(v1)
            found_idx = idx if idx != -1 else None
            return (f"Found {v1} at position {idx}" if idx != -1 else f"{v1} not found"), found_idx, None

    # ---------------- Doubly Linked List ----------------
    if ds_name == "Doubly Linked List":
        if trigger == "btn-op1":
            obj.insert_at_beginning(v1)
            return f"Inserted {v1} at beginning", 0, None
        if trigger == "btn-op2":
            obj.insert_at_end(v1)
            return f"Inserted {v1} at end", len(obj.to_list_forward()) - 1, None
        if trigger == "btn-delete":
            ok = obj.delete(v1)
            return (f"Deleted {v1}" if ok else f"{v1} not found"), None, None
        if trigger == "btn-search":
            idx = obj.search(v1)
            found_idx = idx if idx != -1 else None
            return (f"Found {v1} at position {idx}" if idx != -1 else f"{v1} not found"), found_idx, None

    # ---------------- General Tree ----------------
    if ds_name == "Tree":
        if trigger == "btn-op1":
            if obj.root is None:
                obj.add_node(None, v1)
                return f"Added {v1} as root", None, v1
            if v2 is None:
                return "Tree already has a root - type a parent value in the second box.", None, None
            ok = obj.add_node(v2, v1)
            return (f"Added {v1} under {v2}" if ok else f"Parent {v2} not found"), None, v1
        if trigger == "btn-delete":
            ok = obj.delete_node(v1)
            return (f"Deleted {v1}" if ok else f"{v1} not found"), None, None

    # ---------------- BST ----------------
    if ds_name == "Binary Search Tree":
        if trigger == "btn-op1":
            obj.insert(v1)
            return f"Inserted {v1}", None, v1
        if trigger == "btn-delete":
            obj.delete(v1)
            return f"Deleted {v1}", None, None
        if trigger == "btn-search":
            found = obj.search(v1)
            return (f"Found {v1}" if found else f"{v1} not found"), None, (v1 if found else None)
        if trigger == "btn-min":
            m = obj.find_min()
            return (f"Minimum is {m}" if m is not None else "Tree is empty"), None, m
        if trigger == "btn-max":
            m = obj.find_max()
            return (f"Maximum is {m}" if m is not None else "Tree is empty"), None, m

    # ---------------- AVL Tree ----------------
    if ds_name == "AVL Tree":
        if trigger == "btn-op1":
            obj.insert(v1)
            note = f" -> {obj.last_rotation}" if obj.last_rotation else ""
            return f"Inserted {v1}{note}", None, v1
        if trigger == "btn-delete":
            obj.delete(v1)
            note = f" -> {obj.last_rotation}" if obj.last_rotation else ""
            return f"Deleted {v1}{note}", None, None
        if trigger == "btn-search":
            found = obj.search(v1)
            return (f"Found {v1}" if found else f"{v1} not found"), None, (v1 if found else None)

    # ---------------- B+ Tree ----------------
    if ds_name == "B+ Tree":
        if trigger == "btn-op1":
            obj.insert(v1)
            note = " -> a node split happened" if obj.last_split else ""
            return f"Inserted {v1}{note}", None, v1
        if trigger == "btn-search":
            found = obj.search(v1)
            return (f"Found {v1}" if found else f"{v1} not found"), None, (v1 if found else None)

    # ---------------- Graph ----------------
    if ds_name == "Graph":
        if trigger == "btn-op1":
            obj.add_vertex(v1)
            return f"Added vertex {v1}", None, v1
        if trigger == "btn-op2":
            if v2 is None:
                return "Type a second vertex to connect.", None, None
            obj.add_edge(v1, v2)
            return f"Added edge {v1} - {v2}", None, None
        if trigger == "btn-delete":
            obj.delete_vertex(v1)
            return f"Deleted vertex {v1}", None, None
        if trigger == "btn-delete2":
            if v2 is None:
                return "Type a second vertex to remove that edge.", None, None
            obj.delete_edge(v1, v2)
            return f"Deleted edge {v1} - {v2}", None, None

    # ---------------- Hash Table ----------------
    if ds_name == "Hash Table":
        if trigger == "btn-op1":
            idx = obj.insert(v1)
            return f"Inserted {v1} into bucket {idx}", idx, None
        if trigger == "btn-delete":
            idx = obj._hash(v1)
            ok = obj.delete(v1)
            return (f"Deleted {v1} from bucket {idx}" if ok else f"{v1} not found"), idx, None
        if trigger == "btn-search":
            idx, found = obj.search(v1)
            return (f"Found {v1} in bucket {idx}" if found else f"{v1} not found (checked bucket {idx})"), idx, None

    return "", None, None


# ============================================================
# ONE CALLBACK TO RULE THEM ALL
# Handles: switching data structures, every operation button, the
# reset/random-data buttons, running a traversal, and moving the
# step-by-step slider. Kept as a single callback (instead of several
# smaller ones) so that no two callbacks ever try to write to the
# same output at once.
# ============================================================
@app.callback(
    Output("definition-card", "children"),
    Output("complexity-table-container", "children"),
    Output("space-complexity", "children"),
    Output("input-value1", "placeholder"),
    Output("input-value2", "placeholder"),
    Output("input-value2", "style"),
    Output("btn-op1", "children"), Output("btn-op1", "style"),
    Output("btn-op2", "children"), Output("btn-op2", "style"),
    Output("btn-op3", "children"), Output("btn-op3", "style"),
    Output("btn-delete", "children"), Output("btn-delete", "style"),
    Output("btn-delete2", "children"), Output("btn-delete2", "style"),
    Output("btn-search", "style"),
    Output("btn-peek", "children"), Output("btn-peek", "style"),
    Output("btn-min", "style"), Output("btn-max", "style"),
    Output("btn-random", "children"),
    Output("graph-mode-radio", "style"),
    Output("traversal-row", "style"),
    Output("traversal-select", "options"),
    Output("traversal-select", "value"),
    Output("step-slider-container", "style"),
    Output("step-slider", "max"),
    Output("step-slider", "value"),
    Output("traversal-order-store", "data"),
    Output("traversal-order-display", "children"),
    Output("status-message", "children"),
    Output("visualization", "figure"),
    Output("history-store", "data"),
    Output("history-log", "children"),
    Input("ds-selector", "value"),
    Input("btn-op1", "n_clicks"),
    Input("btn-op2", "n_clicks"),
    Input("btn-op3", "n_clicks"),
    Input("btn-delete", "n_clicks"),
    Input("btn-delete2", "n_clicks"),
    Input("btn-search", "n_clicks"),
    Input("btn-peek", "n_clicks"),
    Input("btn-min", "n_clicks"),
    Input("btn-max", "n_clicks"),
    Input("btn-reset", "n_clicks"),
    Input("btn-random", "n_clicks"),
    Input("btn-traverse", "n_clicks"),
    Input("step-slider", "value"),
    State("input-value1", "value"),
    State("input-value2", "value"),
    State("graph-mode-radio", "value"),
    State("traversal-select", "value"),
    State("traversal-order-store", "data"),
    State("history-store", "data"),
)
def main_callback(ds_name, n1, n2, n3, nd, nd2, nsearch, npeek, nmin, nmax, nreset, nrandom,
                   ntraverse, step_value, raw1, raw2, graph_mode, traversal_choice,
                   traversal_data, history):
    trigger = ctx.triggered_id  # None on first page load
    history = history or []

    # ---- everything that depends only on WHICH data structure is selected ----
    cfg = DS_CONTROLS[ds_name]
    info = DS_INFO[ds_name]

    definition_children = [html.Strong(ds_name + ": "), info["definition"]]
    if ds_name == "Hash Table":
        definition_children.append(html.Pre(HASH_TABLE_NOTES, className="hash-notes"))
    space = html.P([html.Strong("Space Complexity: "), info["space"]])

    input2_style = SHOWN if cfg["show_input2"] else HIDDEN
    op2_style = SHOWN if cfg["op2"] else HIDDEN
    op3_style = SHOWN if cfg["op3"] else HIDDEN
    delete_style = SHOWN if cfg["delete"] else HIDDEN
    delete2_style = SHOWN if cfg["delete2"] else HIDDEN
    search_style = SHOWN if cfg["search"] else HIDDEN
    peek_style = SHOWN if cfg["peek"] else HIDDEN
    minmax_style = SHOWN if cfg["minmax"] else HIDDEN
    graph_mode_style = SHOWN if cfg["graph_mode"] else HIDDEN

    if cfg["traversal_options"]:
        traversal_row_style = SHOWN
        traversal_ui_options = [{"label": t, "value": t} for t in cfg["traversal_options"]]
        traversal_ui_value = cfg["traversal_options"][0]
    else:
        traversal_row_style = HIDDEN
        traversal_ui_options = []
        traversal_ui_value = None

    config_outputs = (
        definition_children,
        complexity_table(ds_name),
        space,
        cfg["input1_placeholder"],
        cfg["input2_placeholder"], input2_style,
        cfg["op1"] or "Insert", SHOWN,
        cfg["op2"] or "Op2", op2_style,
        cfg["op3"] or "Op3", op3_style,
        cfg["delete"] or "Delete", delete_style,
        cfg["delete2"] or "Delete2", delete2_style,
        search_style,
        cfg["peek"] or "Peek", peek_style,
        minmax_style, minmax_style,
        cfg["random"],
        graph_mode_style,
    )

    # ---- CASE 1: just switched to a different data structure (or first load) ----
    if trigger in (None, "ds-selector"):
        figure = render_figure(ds_name)
        return config_outputs + (
            traversal_row_style, traversal_ui_options, traversal_ui_value,
            HIDDEN, 0, 0,
            [], "",
            "",
            figure,
            dash.no_update, dash.no_update,   # leave history untouched
        )

    obj = STATE[ds_name]
    v1 = parse_value(raw1)
    v2 = parse_value(raw2)

    # ---- CASE 2: dragging the step-by-step traversal slider ----
    if trigger == "step-slider":
        order = traversal_data or []
        step = min(step_value, max(len(order) - 1, 0)) if order else 0
        visited_so_far = order[: step + 1] if order else []
        current = order[step] if order else None
        figure = render_figure(ds_name, visited_values=visited_so_far, current_value=current)
        return config_outputs + (
            traversal_row_style, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update,
            dash.no_update,
            figure,
            dash.no_update, dash.no_update,
        )

    # ---- CASE 3: Reset ----
    if trigger == "btn-reset":
        if ds_name == "Graph":
            STATE["Graph"] = Graph(directed=(graph_mode == "directed"))
        else:
            obj.reset()
        status = f"{ds_name} has been reset."
        history = push_history(history, ds_name, "Reset")
        figure = render_figure(ds_name)
        return config_outputs + (
            traversal_row_style, dash.no_update, dash.no_update,
            HIDDEN, 0, 0,
            [], "",
            status,
            figure,
            history, render_history(history),
        )

    # ---- CASE 4: Generate Random Data ----
    if trigger == "btn-random":
        status = generate_random(ds_name)
        history = push_history(history, ds_name, "Generated random data")
        figure = render_figure(ds_name)
        return config_outputs + (
            traversal_row_style, dash.no_update, dash.no_update,
            HIDDEN, 0, 0,
            [], "",
            status,
            figure,
            history, render_history(history),
        )

    # ---- CASE 5: Run Traversal ----
    if trigger == "btn-traverse":
        order = traversal_order(ds_name, traversal_choice, start_vertex=v1)
        if not order:
            status = "Nothing to traverse yet - add some data first (or check the start vertex)."
            figure = render_figure(ds_name)
            return config_outputs + (
                traversal_row_style, dash.no_update, dash.no_update,
                HIDDEN, 0, 0,
                [], "",
                status,
                figure,
                history, render_history(history),
            )
        status = f"{traversal_choice}: " + " -> ".join(str(v) for v in order)
        history = push_history(history, ds_name, status)
        figure = render_figure(ds_name, visited_values=[order[0]], current_value=order[0])
        order_display = html.P(f"Order: {' -> '.join(str(v) for v in order)}")
        return config_outputs + (
            traversal_row_style, dash.no_update, dash.no_update,
            SHOWN, max(len(order) - 1, 0), 0,
            order, order_display,
            status,
            figure,
            history, render_history(history),
        )

    # ---- CASE 6: every other operation button (insert/delete/search/peek/min/max) ----
    needs_value = trigger not in ("btn-min", "btn-max", "btn-peek")
    if needs_value and v1 is None:
        status = "Please type a value first."
        figure = render_figure(ds_name)
        return config_outputs + (
            traversal_row_style, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update,
            status,
            figure,
            history, render_history(history),
        )

    status, highlight_index, highlight_value = run_operation(trigger, ds_name, obj, v1, v2)
    if status:
        history = push_history(history, ds_name, status)
    figure = render_figure(ds_name, current_value=highlight_value, highlight_index=highlight_index)

    return config_outputs + (
        traversal_row_style, dash.no_update, dash.no_update,
        dash.no_update, dash.no_update, dash.no_update,
        dash.no_update, dash.no_update,
        status,
        figure,
        history, render_history(history),
    )


if __name__ == "__main__":
    app.run(debug=True)
