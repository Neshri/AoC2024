import time

def construct_memory(data):
    """Constructs the memory array from the input data."""
    memory = []
    i = 0
    while i < len(data):
        block_id = i // 2
        amount = int(data[i])
        memory.extend([block_id] * amount)
        if i + 1 < len(data):
            empty_amount = int(data[i + 1])
            memory.extend([-1] * empty_amount)
        i += 2
    return memory

def compute_checksum(memory):
    """Computes the checksum of the given memory layout."""
    return sum(i * block for i, block in enumerate(memory) if block != -1)

def compact_files(memory):
    """Moves whole files left into the first available free space span."""
    n = len(memory)
    free_spans = []
    i = 0

    # Locate all free spans
    while i < n:
        if memory[i] == -1:
            start = i
            while i < n and memory[i] == -1:
                i += 1
            free_spans.append((start, i - start))
        else:
            i += 1
    right_i = len(memory) - 1
    # Compact files in reverse order of their IDs
    for file_id in range(memory[-1], 0, -1):
        # Locate the file
        while right_i >= 0 and memory[right_i] != file_id:
            right_i -= 1
        if right_i < 0:
            continue

        left_i = right_i
        while left_i >= 0 and memory[left_i] == file_id:
            left_i -= 1
        left_i += 1

        file_size = right_i - left_i + 1

        # Find the first free span that fits the file
        for idx, (start, span_size) in enumerate(free_spans):
            if span_size >= file_size and start < left_i:
                # Move the file to this span
                for j in range(file_size):
                    memory[start + j] = file_id
                    memory[left_i + j] = -1
                # Update the free span
                free_spans[idx] = (start + file_size, span_size - file_size)
                break

# Start measuring time
start_time = time.perf_counter()

# Read input data
with open("day9.txt", "r") as f:
    data = f.readline().strip()

# Construct the initial memory layout
memory = construct_memory(data)

# Solve part one: Move individual blocks
left_i = 0
right_i = len(memory) - 1
while left_i < right_i:
    while memory[left_i] != -1 and left_i < len(memory):
        left_i += 1
    while memory[right_i] == -1 and right_i >= 0:
        right_i -= 1
    if left_i >= right_i:
        break
    memory[left_i], memory[right_i] = memory[right_i], memory[left_i]

# Compute checksum for part one
checksum_part_one = compute_checksum(memory)
print("The first answer is:", checksum_part_one)

# Reconstruct the memory for part two
memory = construct_memory(data)

# Solve part two
compact_files(memory)

# Compute checksum for part two
checksum_part_two = compute_checksum(memory)
print("The second answer is:", checksum_part_two)

# Print execution time
print("Execution time:", "{:.3f}".format(time.perf_counter() - start_time), "seconds")
