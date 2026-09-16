# Data Structures Visualizer

An interactive web app, built with **Python + Dash + Plotly**, that lets you
create and operate on 9 core data structures and *watch* every operation
happen live.

## Live Features

- One dashboard: pick a data structure from the dropdown, and the whole
  page (controls, definition, complexity table, visualization) updates for it.
- **Definition card** — selecting a data structure shows a short, plain
  explanation of what it is right above the controls.
- Real operations, not fake animations — every button calls a real Python
  method (`push`, `enqueue`, `insert`, `bfs`, ...) on a real object kept on
  the server, and the chart re-renders from the object's actual state.
- Visual feedback: newly-inserted nodes, the current node, and
  visited/found nodes are colour-coded (see the legend colours in
  `visualizations.py`).
- Step-by-step traversal: for trees and graphs, running a traversal
  (Preorder, BFS, DFS, ...) fills a slider you can drag to walk through
  the visit order one step at a time.
- "Generate Random Data" button per structure, to see a populated
  example instantly.
- Operation history log (last 12 actions) and a time/space complexity
  table that updates per structure.

## Data Structures Included

Queue, Stack, Singly Linked List, Doubly Linked List, (general) Tree,
Binary Search Tree, AVL Tree, a simplified B+ Tree, Graph (BFS/DFS,
directed or undirected), and a Hash Table (chaining for collisions).

## Project Structure

```
ds_visualizer/
├── app.py                    # Dash layout + the single callback that wires it up
├── visualizations.py         # Turns a structure's state into a Plotly figure
├── info.py                   # Definitions + complexity tables shown in the UI
├── test_data_structures.py   # Quick sanity tests for every data structure
├── assets/
│   └── style.css             # Styling (Dash auto-loads anything in /assets)
├── requirements.txt
│
└── data_structures/          # One file per data structure
    ├── __init__.py           # Re-exports every class from one place
    ├── queue_ds.py            # Queue
    ├── stack.py                # Stack
    ├── singly_linked_list.py   # Singly Linked List
    ├── doubly_linked_list.py   # Doubly Linked List
    ├── tree.py                 # General Tree
    ├── bst.py                  # Binary Search Tree
    ├── avl_tree.py              # AVL Tree
    ├── bplus_tree.py            # B+ Tree
    ├── graph.py                 # Graph
    └── hash_table.py            # Hash Table
```

Each data structure has its own file — open `data_structures/stack.py`
if you only want to see how the Stack works, without scrolling past
nine other classes. `data_structures/__init__.py` re-exports every
class, so `app.py` still writes one simple line:
`from data_structures import Queue, Stack, BST, ...` — it doesn't
need to know which individual file each class actually lives in.

## Running Locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open the URL printed in the terminal (usually
`http://127.0.0.1:8050`).

You can also run the logic tests on their own, with no Dash/Plotly
installed at all:

```bash
python test_data_structures.py
```

## Putting it on GitHub

```bash
git init
git add .
git commit -m "Data Structures Visualizer - initial version"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Deploying Online (Render, free tier)

1. Push the project to GitHub (above).
2. Go to [render.com](https://render.com) → **New → Web Service** → connect
   your repo.
3. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:server`
4. Deploy. Render will give you a public URL.

(Railway and PythonAnywhere work the same way — install
`requirements.txt`, then run the app with a WSGI server pointed at
`app:server`, since `server = app.server` is already exposed in
`app.py`.)

## Notes on Design Choices (for the report / documentation section)

- **State:** each data structure is kept as one live Python object on the
  server (see `STATE` in `app.py`). This is intentionally simple for a
  single-user class project; a production multi-user version would keep
  this state per browser session instead of in one global dictionary.
- **B+ Tree:** simplified — fixed order, keys only (no separate
  key/value pairs) — since a full production B+ Tree (with disk pages,
  deletion re-balancing, etc.) is out of scope for a teaching visualizer.
- **Hash Table:** collisions are resolved with **chaining** (each bucket
  is a small list); `hash(key) % table_size` is the hash function.
- **Tree layout:** node x-position is the average of its children's
  x-positions (children get sequential positions), and y is `-depth` —
  a simple, readable way to lay out a tree without external graph
  libraries.
