import tkinter as tk


def dfs(adj, visited, u):
    nodes = list(adj.keys())

    for node in nodes:
        if node < 0 or node >= len(visited):
            raise ValueError("Nodes must be numbered from 0 to len(adj) - 1.")

        for neighbor in adj[node]:
            if neighbor not in adj:
                raise ValueError(f"Node {neighbor} is missing from adj.")

    if u not in adj:
        raise ValueError(f"Start node {u} does not exist.")

    children = {node: [] for node in nodes}
    parents = {}
    depths = {}

    def organize_tree(node, parent=None, depth=0):
        if node in parents:
            raise ValueError("The adjacency list must describe a tree.")

        parents[node] = parent
        depths[node] = depth

        for neighbor in adj[node]:
            if neighbor == parent:
                continue

            children[node].append(neighbor)
            organize_tree(neighbor, node, depth + 1)

    organize_tree(u)

    if len(parents) != len(nodes):
        raise ValueError("The tree must be connected.")

    events = []
    planned = {node: bool(visited[node]) for node in nodes}

    def build_events(node):
        if planned[node]:
            return

        planned[node] = True
        events.append(("visit", node))

        for child in children[node]:
            build_events(child)

        events.append(("backtrack", node))

    build_events(u)

    root = tk.Tk()
    root.title("Algorithm Visualizer - DFS")
    root.geometry("1100x700")
    root.configure(bg="#111827")

    title = tk.Label(
        root,
        text="DEPTH-FIRST SEARCH",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#111827"
    )
    title.pack(pady=15)

    body = tk.Frame(root, bg="#111827")
    body.pack(fill="both", expand=True, padx=15, pady=10)

    canvas = tk.Canvas(
        body,
        bg="#111827",
        highlightthickness=0
    )
    canvas.pack(side="left", fill="both", expand=True)

    side = tk.Frame(body, bg="#1F2937", width=260)
    side.pack(side="right", fill="y", padx=(12, 0))
    side.pack_propagate(False)

    status = tk.Label(
        side,
        text=f"Starting at node {u}",
        font=("Arial", 13, "bold"),
        fg="white",
        bg="#1F2937",
        wraplength=230
    )
    status.pack(padx=12, pady=18)

    tk.Label(
        side,
        text="TRAVERSAL LOG",
        font=("Arial", 11, "bold"),
        fg="white",
        bg="#1F2937"
    ).pack(pady=5)

    log = tk.Listbox(
        side,
        bg="#111827",
        fg="white",
        font=("Menlo", 10),
        borderwidth=0,
        highlightthickness=0
    )
    log.pack(fill="both", expand=True, padx=12, pady=10)

    tk.Label(
        side,
        text="BLUE  Current node\nORANGE  Visited\nGRAY  Unvisited",
        justify="left",
        font=("Arial", 11),
        fg="white",
        bg="#1F2937"
    ).pack(anchor="w", padx=12, pady=15)

    root.update_idletasks()

    width = max(canvas.winfo_width(), 700)
    height = max(canvas.winfo_height(), 500)

    leaf_positions = {}
    leaf_index = 0

    def assign_leaf_positions(node):
        nonlocal leaf_index

        if not children[node]:
            leaf_positions[node] = leaf_index
            leaf_index += 1
            return leaf_positions[node]

        positions = [
            assign_leaf_positions(child)
            for child in children[node]
        ]

        leaf_positions[node] = sum(positions) / len(positions)
        return leaf_positions[node]

    assign_leaf_positions(u)

    leaf_count = leaf_index
    max_depth = max(depths.values())
    positions = {}

    margin_x = 45
    margin_y = 45
    usable_width = width - 2 * margin_x
    usable_height = height - 2 * margin_y

    for node in nodes:
        x = margin_x + (
            leaf_positions[node] / max(leaf_count - 1, 1)
        ) * usable_width

        y = margin_y + (
            depths[node] / max(max_depth, 1)
        ) * usable_height

        positions[node] = (x, y)

    for node in nodes:
        for child in children[node]:
            x1, y1 = positions[node]
            x2, y2 = positions[child]

            canvas.create_line(
                x1, y1, x2, y2,
                fill="#6B7280",
                width=2
            )

    node_radius = 22
    circles = {}

    visited_nodes = {
        node for node in nodes if visited[node]
    }
    current_node = None

    def redraw():
        for node, circle in circles.items():
            if node == current_node:
                color = "#2563EB"
            elif node in visited_nodes:
                color = "#F59E0B"
            else:
                color = "#374151"

            canvas.itemconfig(circle, fill=color)

    for node in nodes:
        x, y = positions[node]

        circle = canvas.create_oval(
            x - node_radius,
            y - node_radius,
            x + node_radius,
            y + node_radius,
            fill="#374151",
            outline="white",
            width=2
        )

        canvas.create_text(
            x, y,
            text=str(node),
            fill="white",
            font=("Arial", 12, "bold")
        )

        circles[node] = circle

    step_index = 0

    def step():
        nonlocal step_index, current_node

        if step_index >= len(events):
            current_node = None
            redraw()
            status.config(text="DFS completed!")
            log.insert(tk.END, "DFS completed!")
            log.yview_moveto(1)
            return

        action, node = events[step_index]
        step_index += 1

        if action == "visit":
            current_node = node
            visited_nodes.add(node)
            visited[node] = True
            message = f"Visiting node: {node}"

        else:
            visited_nodes.discard(node)
            visited[node] = False
            current_node = parents[node]
            message = f"Backtracking from node: {node}"

        print(message)
        status.config(text=message)
        log.insert(tk.END, message)
        log.yview_moveto(1)

        redraw()
        root.after(500, step)

    redraw()
    root.after(500, step)
    root.mainloop()