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


steps = open("inputs.txt").read().split(",")

sum_of_hashes = 0
for step in steps:
    sum_of_hashes += hash(step)
print(sum_of_hashes)
