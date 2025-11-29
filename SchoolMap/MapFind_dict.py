import csv 

class SchoolGraph: 
    def __init__(self, csv_path: str): 
        # adjacenct list: vertex index -> list of neighbor indices 
        self.adj: dict[int, list[int]] = {}     # stores adjacency list  (keys/vertex indices are integers, values are lists of integers (neighbors))
        # mapping between indices and human-readable names 
        self.idx_to_name: dict[int, str] = {}       # maps vertext index -> room name (ex. 0 -> "Rose Atrium")
        self.name_to_idx: dict[str, int] = {}       # maps room name -> vertex index (ex. "Rose Atrium" -> 0) useful for searching by name later 

        self._load_from_csv(csv_path)   # helper function to read the CSV file 

    def _load_from_csv(self, csv_path: str) -> None:    # underscore means private function
        '''Read the CSV file and build the adjacency list'''
        with open(csv_path, newline='') as f:   # opens csv file, newline='' avoids formatting issues, calling the file object f
            reader = csv.DictReader(f)  #reads each row 
            '''{
            "idx": "0",
            "vertex_name": "Rose Atrium",
            "adjacencies": "1,2,3,...",
            "Degree": "10",
            "Max Degree": "34"
            }'''

            for row in reader:  # loop through each row 
                # 1. Parse the vertex index and name , none means function doesn't return anything 
                idx = int(row["idx"])       # every value from CSV is a string, so we convert it to an integer
                name = row["vertex_name"].strip()       # .strip() removes extra spaces 

                self.idx_to_name[idx] = name  
                self.name_to_idx[name] = idx        # save name mappings both direction index->name and name->index
            
                #2. Parse the adjacenceis field: "1, 2, 3" or "0" 
                neighbors_str = str(row["adjacencies"]).strip()     # get adjacency list string (ex. "1, 2, 3, 20, 163")
                neighbors: list[int] = []       # start a list for neighbors [1, 2, 3, 4]

                if neighbors_str != "":     # skip row with no neighbors 
                    # split on commas, convert each part to int 
                    for part in neighbors_str.split(","):   # splits "1, 2, 3" into ["1", "2", "3"]
                        part = part.strip()
                        if part == "":
                            continue 
                        neighbors.append(int(part))     #clean whitespeace, convert each piece to an integer, add to neighbor list

                #3. Store in adjacency list 
                self.adj[idx] = neighbors   # store in adjacency list  (ex. self.adj[0] = [1,2,3,4,5,6,7,8,20,163])

    # other functions 
    def neighbors_by_index(self, idx: int) -> list[int]:        # look up neighbors using index
        '''Return neighbor indices for a vertex index'''
        return self.adj.get(idx, [])
    
    def neighbors_by_name(self, name: str) -> list[str]:        # look up neighbors using name (convert name to index, get numeric neighbors, neighbor back to name)
        '''Return neighbor names for a given room name'''
        idx = self.name_to_idx[name]
        return [self.idx_to_name[n] for n in self.adj.get(idx, [])]
    
    def num_vertices(self) -> int:      #count number of vertices, how many keys are in the adjacency list
        return len(self.adj)
    
    def as_list_of_lists(self) -> list[list[int]]:
        '''Return adjacency list as a 0-indexed list of lists.'''
        n = max(self.adj.keys()) + 1
        adj_list = [[] for _ in range(n)]
        for idx, neighbors in self.adj.items():
            adj_list[idx] = neighbors
        return adj_list

# ------------------------------------------------------------------
# Breadth-First Search (BFS): find a path from start to end
# Explore graph level by level: First check all rooms 1 hallway away, then 2 hallways, then 3 hallways
# ------------------------------------------------------------------

    def bfs_path(self, start_name: str, end_name: str) -> list  [str] | None: # takes two room names and returns list of room names if a path exists 
        """Return a path of vertex names from start_name to end_name using BFS.
        If no path exists, return None.
        """
        start = self.name_to_idx[start_name]    #convert human room names to graph vertex indices 
        end = self.name_to_idx[end_name]

        from collections import deque   # queue structure that allows for more efficient pops from the front 

        # queue: rooms to visit next , visited: keeps track of rooms already seen, parent: what led to room 
        queue = deque()           # queue of vertex indices to explore
        visited: set[int] = set() # to avoid revisiting vertices
        parent: dict[int, int] = {}  # child_idx -> parent_idx (who led to room)

        # initialize BFS: Start at the starting room, Mark it as visited, Put it in the queue to be explored
        queue.append(start)
        visited.add(start)

        while queue:
            current = queue.popleft()   # Remove the first item in the queue - this is what lets BFS go in levels 

            # if we reached the goal, stop searching
            if current == end:
                break

            # explore neighbors: self.adj is your adjacency list (Look at all rooms connected to the current room)
            for neighbor in self.adj.get(current, []):
                if neighbor not in visited:     # skip neighbors we have seen already 
                    visited.add(neighbor)       # For every unvisited neighbor: Mark it visited, Remember that we came from current, Add it to the queue so BFS will explore it later
                    parent[neighbor] = current
                    queue.append(neighbor)

        # if we never reached 'end', there is no path
        if end not in visited:
            return None

        # reconstruct path from end back to start using parent links
        path_indices: list[int] = []
        cur = end
        while True:
            path_indices.append(cur)
            if cur == start:
                break
            cur = parent[cur]

        # reverse to get start -> ... -> end
        path_indices.reverse()

        # convert indices to room names
        return [self.idx_to_name[i] for i in path_indices]
    

# ------------------------------------------------------------------
 # Depth-First Search (DFS): find a path from start to end
 # Goes in one direction as far as possible, Backtracks when it hits a dead-end, Tries a new direction, Continues until it finds the end
# ------------------------------------------------------------------
    def dfs_path(self, start_name: str, end_name: str) -> list[str] | None:
        """Return a path of vertex names from start_name to end_name using DFS.
        If no path exists, return None.
        """
        start = self.name_to_idx[start_name]
        end = self.name_to_idx[end_name]

        visited: set[int] = set()   # visited: avoid cycles, parent: reconstruct path later
        parent: dict[int, int] = {}

        # recursive helper function
        # Mark the current room visited. If it is the destination → we’re done
        def dfs(current: int) -> bool:
            visited.add(current)
            if current == end:
                return True  # found the target

            # Try each neighbor. If not visited: mark parent, recursively search DFS down that neighbor, If any child returns True → we found a path
            for neighbor in self.adj.get(current, []):
                if neighbor not in visited:
                    parent[neighbor] = current
                    if dfs(neighbor):
                        return True  # bubble up success

            return False  # no path from this branch

        # run DFS starting at 'start'
        found = dfs(start)

        if not found:
            return None

        # reconstruct path just like in BFS
        path_indices: list[int] = []
        cur = end
        while True:
            path_indices.append(cur)
            if cur == start:
                break
            cur = parent[cur]

        path_indices.reverse()
        return [self.idx_to_name[i] for i in path_indices]

    # optional: how many vertices are in this graph?
    def num_vertices(self) -> int:
        return len(self.adj)


# ---------------------------------------------------------------
# DFS SPANNING TREE (returns adjacency list)
# ---------------------------------------------------------------
    def dfs_spanning_tree(self, start_name: str) -> dict[int, list[int]]:
        start = self.name_to_idx[start_name]
        visited: set[int] = set()
        parent: dict[int, int] = {}

        def dfs(current: int) -> None:
            visited.add(current)
            for neighbor in self.adj.get(current, []):
                if neighbor not in visited:
                    parent[neighbor] = current
                    dfs(neighbor)

        dfs(start)

        # Build tree adjacency list
        tree_adj: dict[int, list[int]] = {v: [] for v in visited}
        for child, par in parent.items():
            tree_adj[par].append(child)
            tree_adj[child].append(par)

        return tree_adj
# ---------------------------------------------------------------
# convert spanning tree to names instead of indices
# ---------------------------------------------------------------
    def spanning_tree_names(self, tree_adj: dict[int, list[int]]) -> dict[str, list[str]]:
        name_adj: dict[str, list[str]] = {}
        for idx, neighbors in tree_adj.items():
            room_name = self.idx_to_name[idx]
            name_adj[room_name] = [self.idx_to_name[n] for n in neighbors]
        return name_adj

if __name__ == "__main__":
    graph = SchoolGraph("HM_Graph.csv")

    print("Number of rooms (vertices):", graph.num_vertices())

    start = "Olshan Lobby"          
    end = "Recording Studio Room 1" 

    bfs_result = graph.bfs_path(start, end)
    dfs_result = graph.dfs_path(start, end)

    print(f"\nBFS path from {start} to {end}:")
    print(bfs_result)

    print(f"\nDFS path from {start} to {end}:")
    print(dfs_result)

    # Spanning trees
    bfs_tree = graph.bfs_spanning_tree(start)
    dfs_tree = graph.dfs_spanning_tree(start)

    print("\nBFS Spanning Tree (by room names):")
    print(graph.spanning_tree_names(bfs_tree))

    print("\nDFS Spanning Tree (by room names):")
    print(graph.spanning_tree_names(dfs_tree))