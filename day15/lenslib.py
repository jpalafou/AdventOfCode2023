def hash(s: str) -> int:
    """
    args:       s       any string
    returns:    out     hash integer
    """
    out = 0
    for c in s:
        out += ord(c)
        out = (out * 17) % 256
    return out


class Lens:
    def __init__(self, label: str, focal_length: int = None):
        """
        args:
            label           series of lowercase letters
            focal_length    optional
        """
        self.label = label
        self.focal_length = focal_length

    def __eq__(self, other):
        return self.label == other.label


steps = open("inputs.txt").read().split(",")

# compute the sum of the hashes of each step
sum_of_hashes = 0
for step in steps:
    sum_of_hashes += hash(step)
print(sum_of_hashes)


# place each lens in its correct box according to the initialization sequence
boxes = []
for _ in range(256):
    boxes.append([])

for step in steps:
    if "-" in step:
        label, _ = step.split("-")
        i = hash(label)
        lens = Lens(label)
        if lens in boxes[i]:
            boxes[i].remove(lens)
    elif "=" in step:
        label, length = step.split("=")
        i = hash(label)
        lens = Lens(label, int(length))
        if lens in boxes[i]:
            boxes[i][boxes[i].index(lens)] = lens
        else:
            boxes[i].append(lens)


# add up the focusing power of each lens
focusing_power = 0
for i, box in enumerate(boxes):
    for j, lens in enumerate(box):
        focusing_power += (i + 1) * (j + 1) * lens.focal_length
print(focusing_power)
