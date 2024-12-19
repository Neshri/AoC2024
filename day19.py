import time

def count_pattern_combinations(pattern: str, towels: set, pattern_memory: dict) -> int:
    def dive(pattern: str, index: int = 0) -> int:
        if index == len(pattern):
            return 1
        if pattern[index:] in pattern_memory:
            return pattern_memory[pattern[index:]]
        pattern_memory[pattern[index:]] = 0
        for towel in towels:
            if pattern[index:].startswith(towel):
                pattern_memory[pattern[index:]] += dive(pattern, index + len(towel))
        return pattern_memory[pattern[index:]]

    return dive(pattern)

# Input parsing
start_time = time.perf_counter()
towels = set()
patterns = []
with open("day19.txt") as f:
    for line in f:
        line = line.strip()
        if "," in line:
            towels.update(map(str.strip, line.split(", ")))
        elif line:
            patterns.append(line)

# Part 1: Count possible designs
pattern_memory = {}
possible_designs = 0
for design in patterns:
    if count_pattern_combinations(design, towels, pattern_memory) > 0:
        possible_designs += 1

# Part 2: Total combinations for all designs
total_combinations = sum(pattern_memory[design] for design in patterns if design in pattern_memory)

print("The first answer is:", possible_designs)
print("The second answer is:", total_combinations)
print("Execution time:", "{:.3f}".format(time.perf_counter() - start_time), "seconds")
