with open("inputs.txt") as file:
    network = {}
    for line_number, line in enumerate(file):
        stripped_line = line.strip()
        if stripped_line == "":
            # ignore empty lines
            continue
        elif line_number == 0:
            # get sequence of instructions
            translated_line = stripped_line.translate({ord("L"): "0", ord("R"): "1"})
            sequence = list(map(int, translated_line))
            sequence_length = len(sequence)
        else:
            # add each binary to network
            starting_node, next_nodes = stripped_line.split(" = ")
            removed_paranthesis = next_nodes.translate({ord("("): "", ord(")"): ""})
            nodes_pair = tuple(removed_paranthesis.split(", "))
            if nodes_pair == (starting_node, starting_node):
                # node leads to itself
                network[starting_node] = ("...", "...")
                # node leads to at least one other node
            else:
                network[starting_node] = nodes_pair

# walk through network by calling a dictionary whose items are tuples of keys
i = 0
current_node = "AAA"
while current_node not in ["ZZZ", "..."]:
    current_node = network[current_node][sequence[i % sequence_length]]
    i += 1

# show step count if the sequence didn't result in '...'
if current_node == "ZZZ":
    print(f"Got to ZZZ in {i} steps")
else:
    print(f"Found endless loop in {i} steps")
