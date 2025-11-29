import csv

class SchoolGraph:
    def __init__(self, n_vertices: int):
        # adjacency list: index -> list of neighbor indices
        self.adj: list[list[int]] = [[] for _ in range(n_vertices)]
        # room names: index -> room name string
        self.vertex_names: list[str | None] = [None] * n_vertices

    def add_vertex(self, idx: int, name: str):
        self.vertex_names[idx] = name

    def add_edges_from_string(self, idx: int, adjacency_string: str):
        """
        Parse a string like '1,2,3,4' into [1,2,3,4] and store it
        as the adjacency list for vertex idx.
        """
        adjacency_string = adjacency_string.strip()
        if adjacency_string == "":
            return

        neighbors = []
        for part in adjacency_string.split(","):
            part = part.strip()
            if part == "":
                continue
            neighbors.append(int(part))
        self.adj[idx] = neighbors

    def neighbors(self, idx: int) -> list[int]:
        return self.adj[idx]

    def __len__(self):
        return len(self.adj)


def load_school_graph_from_csv(filename: str) -> SchoolGraph:
    # First pass: read all rows so we know the max index
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Find how big the graph needs to be
    max_idx = max(int(row["idx"]) for row in rows)
    graph = SchoolGraph(max_idx + 1)

    # Second pass: fill in names and adjacency lists
    for row in rows:
        idx = int(row["idx"])
        name = row["vertex_name"]
        adj_str = row["adjacencies"]

        graph.add_vertex(idx, name)
        graph.add_edges_from_string(idx, adj_str)

    return graph

graph = load_school_graph_from_csv("HM_Graph.csv")

# Example: print neighbors of vertex 0 ("Rose Atrium")
i = 0
print("Room:", graph.vertex_names[i])
print("Neighbors (by index):", graph.neighbors(i))
print("Neighbors (by name):")
for n in graph.neighbors(i):
    print("  -", n, "->", graph.vertex_names[n])
