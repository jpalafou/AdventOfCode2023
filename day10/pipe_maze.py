import numpy as np

pipe_mating = {
    "|": ("south", "north"),
    "-": ("east", "west"),
    "L": ("north", "east"),
    "J": ("north", "west"),
    "7": ("south", "west"),
    "F": ("south", "east"),
    ".": (),
}
opposite_directions = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
}
kernel = {"north": (-1, 0), "south": (1, 0), "east": (0, 1), "west": (0, -1)}


def infer_pipe_type(neighbors: dict) -> str:
    """
    args:
        neighbors   {north: Pipe1, south: Pipe2, ...}
    returns
        first attempted pipe type which connects to two neighbors
    """
    for pipe_str in pipe_mating.keys():
        pipe = Pipe(pipe_str)
        connections = 0
        for direction, neighbor_pipe in neighbors.items():
            if pipe.is_connected(neighbor_pipe, direction):
                connections += 1
        if connections == 2:
            return pipe


class Pipe:
    def __init__(self, s: str):
        """
        args:
            s   "|", "-", "L", "J", "7", "F", "."
        """
        self.s = s
        self.has_ports = pipe_mating[s]

    def __repr__(self):
        return self.s

    def is_connected(self, other, direction: str) -> bool:
        """
        args:
            other       Pipe
            direction   "north", "south", "east", "west"
        returns:
            whether the specified directional face of self pipe can mate with other
        """
        self_can_connect = direction in self.has_ports
        other_can_connect = opposite_directions[direction] in other.has_ports
        if self_can_connect and other_can_connect:
            return True
        return False


class UnweightedGraph:
    def __init__(self):
        self.adjacency = {}

    def add_node(self, label: str, neighbors: tuple = (), data: list = None):
        """
        args:
            label       index of adjaceny dict
            neighbors   nodes connected to label by an edge
            data        anything else you want to associate with the node
        """
        self.adjacency[label] = {"neighbors": neighbors, "data": data}

    def add_edge(self, label1, label2, undirected: bool = True):
        """
        args:
            label1      starting node
            label2      destination node
            undirected  creates an opposite edge if true
        """
        if label1 not in self.adjacency.keys():
            raise Exception(f"Label {label1} does not exist.")
        if label2 in self.adjacency[label1]["neighbors"]:
            return
        if label1 == label2:
            return
        self.adjacency[label1]["neighbors"] = self.adjacency[label1]["neighbors"] + (
            label2,
        )
        if undirected:
            self.add_edge(label2, label1)

    def dijkstra(
        self,
        starting_node: str,
        target_node: str,
        dont_visit: list = [],
    ) -> list:
        """
        args:
            starting_node
            target_node
            dont_visit      any nodes that should not be visited
        returns:
            path of nodes from starting_node to target_node
        """
        # initialize
        unvisited = set(
            node for node in self.adjacency.keys() if node not in dont_visit
        )
        distances = {node: np.inf for node in unvisited}
        distances[starting_node] = 0
        current_node = starting_node

        while target_node in unvisited:
            # consider all unvisited neighbors
            for neighbor_node in self.adjacency[current_node]["neighbors"]:
                if neighbor_node in unvisited:
                    tentative_distance = distances[current_node] + 1
                    distances[neighbor_node] = min(
                        distances[neighbor_node], tentative_distance
                    )
            unvisited.remove(current_node)
            current_node = min(unvisited, key=lambda key: distances[key])

        # reconstruct path
        reverse_path = [target_node]
        while reverse_path[-1] != starting_node:
            neighbors = [
                x
                for x in self.adjacency[reverse_path[-1]]["neighbors"]
                if x not in dont_visit
            ]
            closest_neighbor = min(neighbors, key=lambda key: distances[key])
            reverse_path.append(closest_neighbor)
        path = reverse_path[::-1]
        return path


# loop through pipe strings and add nodes to graph
graph = UnweightedGraph()
with open("inputs.txt") as file:
    lines = file.readlines()
    pipe_strings = [line.strip() for line in lines]
    nrows, ncols = len(pipe_strings), len(pipe_strings[0])
    for i, row in enumerate(pipe_strings):
        for j, pipe_str in enumerate(row):
            if pipe_str == "S":
                Sidx = (i, j)
                graph.add_node(label=(i, j), data=Pipe("."))
            else:
                graph.add_node(label=(i, j), data=Pipe(pipe_str))

# replace S with its correct pipe type
neighbors = {}
for dir, adjust in kernel.items():
    i, j = Sidx[0] + adjust[0], Sidx[1] + adjust[1]
    if 0 <= i < nrows and 0 <= j < ncols:
        neighbors[dir] = graph.adjacency[(i, j)]["data"]
    else:
        neighbors[dir] = Pipe(".")
new_pipe = infer_pipe_type(neighbors)
graph.add_node(label=Sidx, data=new_pipe)
print(f"Replaced S at {Sidx} with {new_pipe}")

# add edges to graph
for i in range(nrows):
    for j in range(ncols):
        current_pipe = graph.adjacency[(i, j)]["data"]
        for dir, adjust in kernel.items():
            neighbor_idx = (i + adjust[0], j + adjust[1])
            if 0 <= neighbor_idx[0] < nrows and 0 <= neighbor_idx[1] < ncols:
                neighbor_pipe = graph.adjacency[neighbor_idx]["data"]
            else:
                neighbor_pipe = Pipe(".")
            if current_pipe.is_connected(neighbor_pipe, dir):
                graph.add_edge((i, j), neighbor_idx)

# find furthest pipe from S
path = graph.dijkstra(
    starting_node=graph.adjacency[Sidx]["neighbors"][0],
    target_node=graph.adjacency[Sidx]["neighbors"][1],
    dont_visit=[Sidx],
)
assert len(path) % 2 == 1  # path length should be odd
print(f"# steps to furthest pipe: {len(path) // 2 + 1}")
