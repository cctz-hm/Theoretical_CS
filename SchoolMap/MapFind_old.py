import csv
from collections import defaultdict
from typing import Dict, List


class SchoolGraph:
    """
    Graph represented by an adjacency list:
        adj[room_name] = list of neighboring room_names
    """

    def __init__(self) -> None:
        # Map from room name to list of neighbors (room names)
        self.adj: Dict[str, List[str]] = defaultdict(list)

    def add_edge(self, u: str, v: str, undirected: bool = True) -> None:
        """Add an edge between room u and room v."""
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if undirected:
            if u not in self.adj[v]:
                self.adj[v].append(u)

    def neighbors(self, room: str) -> List[str]:
        """Return the neighbors of a given room."""
        return self.adj.get(room, [])

    def rooms(self) -> List[str]:
        """Return all room names in the graph."""
        return list(self.adj.keys())


def load_school_graph_from_csv(path: str) -> SchoolGraph:
    """
    Load the graph from HM_Graph.csv.

    Expected columns:
        idx,vertex_name,adjacencies,Degree,Max Degree

    - idx: integer ID for the node
    - vertex_name: room name (string)
    - adjacencies: comma-separated list of neighbor indices
                   e.g. "1,2,3" or "0"
    """
    graph = SchoolGraph()

    # 1) First pass: build index -> room_name mapping and store raw adjacency indices
    index_to_name: Dict[int, str] = {}
    raw_adj: Dict[int, List[int]] = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx_str = (row.get("idx") or "").strip()
            name = (row.get("vertex_name") or "").strip()
            adj_str = (row.get("adjacencies") or "").strip()

            # skip empty or malformed rows
            if idx_str == "" or name == "":
                continue

            try:
                idx = int(idx_str)
            except ValueError:
                continue

            index_to_name[idx] = name

            if adj_str == "":
                raw_adj[idx] = []
            else:
                # split the "1,2,3" string into integers
                neighbors = []
                for piece in adj_str.split(","):
                    piece = piece.strip()
                    if piece == "":
                        continue
                    try:
                        neighbors.append(int(piece))
                    except ValueError:
                        # ignore any weird values
                        continue
                raw_adj[idx] = neighbors

    # 2) Second pass: convert index-based adjacency into name-based edges
    for u_idx, neighbors in raw_adj.items():
        u_name = index_to_name.get(u_idx)
        if u_name is None:
            continue
        for v_idx in neighbors:
            v_name = index_to_name.get(v_idx)
            if v_name is None:
                continue
            # Undirected edge between room names
            graph.add_edge(u_name, v_name, undirected=True)

    return graph

if __name__ == "__main__":
    g = load_school_graph_from_csv("HM_Graph.csv")

    # See all rooms
    print("Number of rooms:", len(g.rooms()))

    # Example: print neighbors of a specific room
    room = "1st Floor Lutnick"
    print(f"Neighbors of {room}:")
    for n in g.neighbors(room):
        print("  -", n)

    # Access the raw adjacency list directly
    # print(g.adj)
