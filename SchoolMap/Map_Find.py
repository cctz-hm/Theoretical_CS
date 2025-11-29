import csv 
from collections import deque

class SchoolGraph: 
    def __init__(self, csv_path: str): 
        self.adj: dict[int, list[int]] = {}     
        self.idx_to_name: dict[int, str] = {}       
        self.name_to_idx: dict[str, int] = {}     

        self._load_from_csv(csv_path)   

    def _load_from_csv(self, csv_path: str) -> None:   
        '''Read the CSV file and build the adjacency list'''
        with open(csv_path, newline='') as f:  
            reader = csv.DictReader(f)  
            '''{
            "idx": "0",
            "vertex_name": "Rose Atrium",
            "adjacencies": "1,2,3,...",
            "Degree": "10",
            "Max Degree": "34"
            }'''

            for row in reader:  
                # 1. Parse the vertex index and name
                idx = int(row["idx"])       
                name = row["vertex_name"].strip()      

                self.idx_to_name[idx] = name  
                self.name_to_idx[name] = idx       
            
                #2. Parse the adjacenceis field: "1, 2, 3" or "0" 
                neighbors_str = str(row["adjacencies"]).strip()   
                neighbors: list[int] = []     

                if neighbors_str != "":    
                   
                    for part in neighbors_str.split(","):  
                        part = part.strip()
                        if part == "":
                            continue 
                        neighbors.append(int(part))  

                #3. Store in adjacency list 
                self.adj[idx] = neighbors  

    # other functions 
    def neighbors_by_index(self, idx: int) -> list[int]:       
        '''Return neighbor indices for a vertex index'''
        return self.adj.get(idx, [])
    
    def neighbors_by_name(self, name: str) -> list[str]:     
        '''Return neighbor names for a given room name'''
        idx = self.name_to_idx[name]
        return [self.idx_to_name[n] for n in self.adj.get(idx, [])]
    
    def num_vertices(self) -> int:      
        return len(self.adj)
    
    def as_list_of_lists(self) -> list[list[int]]:
        '''Return adjacency list as a 0-indexed list of lists.'''
        n = max(self.adj.keys()) + 1
        adj_list = [[] for _ in range(n)]
        for idx, neighbors in self.adj.items():
            adj_list[idx] = neighbors
        return adj_list

# ------------------------------------------------------------------
# Breadth-First Search (BFS)
# ------------------------------------------------------------------

    def bfs_path(self, start_name: str, end_name: str) -> list[str] | None:
        start = self.name_to_idx[start_name]
        end = self.name_to_idx[end_name]


        queue = deque([start])          
        visited: set[int] = set() 
        parent: dict[int, int] = {} 

        queue.append(start)
        visited.add(start)

        while queue:
            current = queue.popleft() 

            if current == end:
                break

            for neighbor in self.adj.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        

        if end not in visited:
            return None
        
        
        # construct path
        path_indices: list[int] = []
        cur = end
        while True:
            path_indices.append(cur)
            if cur == start:
                break
            cur = parent[cur]

        path_indices.reverse()

        return [self.idx_to_name[i] for i in path_indices]
    

# ------------------------------------------------------------------
 # Depth-First Search (DFS)
# ------------------------------------------------------------------
    def dfs_path(self, start_name: str, end_name: str) -> list[str] | None:
        start = self.name_to_idx[start_name]
        end = self.name_to_idx[end_name]

        visited: set[int] = set()
        parent: dict[int, int] = {}

        # recursive helper function: mark the current room visited
        def dfs(current: int) -> bool:
            visited.add(current)
            if current == end:
                return True 
            
            # try each neighbor. if not visited: mark as parent
            for neighbor in self.adj.get(current, []):
                if neighbor not in visited:
                    parent[neighbor] = current
                    if dfs(neighbor):
                        return True  

            return False  

        found = dfs(start)

        if not found:
            return None

        # construct path
        path_indices: list[int] = []
        cur = end
        while True:
            path_indices.append(cur)
            if cur == start:
                break
            cur = parent[cur]

        path_indices.reverse()
        return [self.idx_to_name[i] for i in path_indices]

    def num_vertices(self) -> int:
        return len(self.adj)


# ---------------------------------------------------------------
# # BFS SPANNING TREE 
# ---------------------------------------------------------------
    def bfs_spanning_tree(self, start_name: str) -> dict[int, list[int]]:
        from collections import deque

        start = self.name_to_idx[start_name]
        queue = deque([start])
        visited: set[int] = {start}
        parent: dict[int, int] = {}

        while queue:
            current = queue.popleft()
            for neighbor in self.adj.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        # Build tree adjacency list
        tree_adj: dict[int, list[int]] = {v: [] for v in visited}
        for child, par in parent.items():
            tree_adj[par].append(child)
            tree_adj[child].append(par)

        return tree_adj


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

    def spanning_tree_names(self, tree_adj: dict[int, list[int]]) -> dict[str, list[str]]:  # convert spanning tree to names instead of indices
        name_adj: dict[str, list[str]] = {}
        for idx, neighbors in tree_adj.items():
            room_name = self.idx_to_name[idx]
            name_adj[room_name] = [self.idx_to_name[n] for n in neighbors]
        return name_adj



# ---------------------------------------------------------------
# ECCENTRICITY
# ---------------------------------------------------------------
    def bfs_distances_from(self, start_idx: int) -> dict[int, int]:
        queue = deque([start_idx])
        # distance to start is 0
        distances: dict[int, int] = {start_idx: 0}

        while queue:
            current = queue.popleft()
            current_dist = distances[current]

            for neighbor in self.adj.get(current, []):
                if neighbor not in distances:
                    # first time we see this neighbor -> record its distance
                    distances[neighbor] = current_dist + 1
                    queue.append(neighbor)

        return distances

    def graph_eccentricity(self) -> int:
        max_distance_overall = 0

        # loop every vertex as a starting point
        for v in self.adj.keys():
            distances = self.bfs_distances_from(v)

            # farthest vertex 
            local_max = max(distances.values())

            if local_max > max_distance_overall:
                max_distance_overall = local_max

        return max_distance_overall
    
if __name__ == "__main__":
    graph = SchoolGraph("HM_Graph.csv")

    print("Number of rooms (vertices):", graph.num_vertices())

    start_idx = 0
    adj_list = graph.as_list_of_lists()
    print("Room name:", graph.idx_to_name[start_idx])
    print("\nNeighbors by index:", graph.neighbors_by_index(start_idx))
    print("Neighbors by name:", graph.neighbors_by_name("Rose Atrium"))
    print(adj_list[0]) 

    start = "Olshan Lobby"          
    end = "Recording Studio Room 1" 

    bfs_result = graph.bfs_path(start, end)
    dfs_result = graph.dfs_path(start, end)

    print(f"\nBFS path from {start} to {end} :")
    print(bfs_result)

    print(f"\nDFS path from {start} to {end} :")
    print(dfs_result)


    # # Spanning trees
    # bfs_tree = graph.bfs_spanning_tree(start)
    # dfs_tree = graph.dfs_spanning_tree(start)

    # print("\nBFS Spanning Tree (by room names):")
    # print(graph.spanning_tree_names(bfs_tree))

    # print("\nDFS Spanning Tree (by room names):")
    # print(graph.spanning_tree_names(dfs_tree))

    ecc = graph.graph_eccentricity()
    print("\nEccentricity of the Horace Mapp graph (in edges):", ecc)


    '''
    Sources: 
    https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/ 
    https://memgraph.com/blog/graph-search-algorithms-developers-guide 
    https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/
    https://www.datacamp.com/tutorial/depth-first-search-in-python
    Used GPT for base code an then edited: https://chatgpt.com/share/692096b1-b88c-800f-ae09-b70118317c6
    
    '''