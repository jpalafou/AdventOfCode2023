import math


def walk_through_network(
    start: str, destination: str, sequence: str, network: dict, max_steps: int
) -> int:
    """
    args:
        start           starting node
        destination     target node
        sequence        series of left/right instructions "LLR.."
        network         keys are strings (must include start and destination)
                        values are pairs of keys (left, right)
                        ("...", "...") indicates that a node leads to itself
        max_steps       stop after this many steps
    returns:
        out             number of steps from start to destination
                        = -1 if "..." was reached
                        = -2 if max_steps was reached
    """
    # map "LLR.." to [0, 0, 1, ...]
    int_string = sequence.translate({ord("L"): "0", ord("R"): "1"})
    sequence_array = list(map(int, int_string))
    sequence_length = len(sequence_array)

    # walk through network
    i = 0
    current_node = start
    while current_node not in [destination, "..."]:
        current_node = network[current_node][sequence_array[i % sequence_length]]
        i += 1
        if current_node == "...":
            return -1
        if i == max_steps:
            return -2
    return i


with open("inputs.txt") as file:
    network = {}
    for line_number, line in enumerate(file):
        stripped_line = line.strip()
        if stripped_line == "":
            # ignore empty lines
            continue
        elif line_number == 0:
            # get sequence of instructions
            sequence = stripped_line
            sequence_length = len(stripped_line)
        else:
            # add each binary to network
            starting_node, next_nodes = stripped_line.split(" = ")
            removed_paranthesis = next_nodes.translate({ord("("): "", ord(")"): ""})
            nodes_pair = tuple(removed_paranthesis.split(", "))
            if nodes_pair == (starting_node, starting_node):
                network[starting_node] = ("...", "...")
            else:
                network[starting_node] = nodes_pair

# walk through network by calling a dictionary whose items are tuples of keys
max_steps = 1000000
steps = walk_through_network(
    start="AAA",
    destination="ZZZ",
    sequence=sequence,
    network=network,
    max_steps=max_steps,
)
print(f"AAA reached ZZZ in {steps} steps")

# which nodes end with A and end in Z, there should be equal amounts of them
endsWithA = [n for n in network.keys() if n[2] == "A"]
endsWithZ = [n for n in network.keys() if n[2] == "Z"]
assert len(endsWithA) == len(endsWithZ)

# find which pairs are connected after some bounded number of steps
connected_nodes = {}
for start in endsWithA:
    for destination in endsWithZ:
        i = walk_through_network(
            start=start,
            destination=destination,
            sequence=sequence,
            network=network,
            max_steps=max_steps,
        )
        if i not in [-1, -2]:
            connected_nodes[(start, destination)] = i
print(f"Verified connected nodes: {[key for key in connected_nodes.keys()]}")

# verify that all step counts are multiples of the sequence length
step_counts = [steps for _, steps in connected_nodes.items()]
assert all(step_count % len(sequence) == 0 for step_count in step_counts)

# find the LCM of each pairs' step period
n_steps_simultaneous = math.lcm(*step_counts)
print(f"All As will reach their destination Zs in {n_steps_simultaneous} steps.")
