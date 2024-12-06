import time

def turn(direction):
    """Turn 90 degrees to the right."""
    return [direction[1], -direction[0]]

def is_outside(pos, data):
    """Check if the position is outside the map bounds."""
    return pos[0] < 0 or pos[0] >= len(data) or pos[1] < 0 or pos[1] >= len(data[0])

def move(pos, direction, data):
    """Simulate the guard's movement."""
    new_pos = [pos[0] + direction[0], pos[1] + direction[1]]
    if is_outside(new_pos, data):
        return False  # Guard leaves the map
    if data[new_pos[0]][new_pos[1]] == "#":
        # Turn right if obstacle
        direction = turn(direction)
        return move(pos, direction, data)  # Try moving again after turn
    return new_pos, direction

def simulate_guard(start_pos, start_dir, data):
    """Simulate the guard's entire patrol."""
    pos = start_pos[:]
    direction = start_dir[:]
    visited = set()
    visited.add(tuple(pos))

    while True:
        result = move(pos, direction, data)
        if not result:
            break  # Guard leaves the map
        pos, direction = result
        visited.add(tuple(pos))

    return visited

from concurrent.futures import ProcessPoolExecutor, as_completed

def test_obstruction(data, start_pos, start_dir, block_pos):
    """Test if placing an obstruction at block_pos causes a loop."""
    y, x = block_pos
    temp_data = [row[:] for row in data]  # Create a copy of the map
    temp_data[y][x] = "#"  # Place obstruction

    visited = set()
    pos = start_pos[:]
    direction = start_dir[:]
    loop_found = False

    while True:
        result = move(pos, direction, temp_data)
        if not result:
            break  # Guard leaves the map
        pos, direction = result
        if (tuple(pos), tuple(direction)) in visited:
            loop_found = True
            break
        visited.add((tuple(pos), tuple(direction)))

    return block_pos if loop_found else None

def find_obstruction_positions_parallel(start_pos, start_dir, data):
    """Find obstruction positions in parallel."""
    # Get the path positions
    pos = start_pos[:]
    direction = start_dir[:]
    path_positions = set()

    while True:
        result = move(pos, direction, data)
        if not result:
            break
        pos, direction = result
        path_positions.add(tuple(pos))

    # Prepare tasks
    valid_positions = [(y, x) for y, x in path_positions if data[y][x] == "." and [y, x] != start_pos]

    # Use ProcessPoolExecutor for parallelism
    blocks = set()
    with ProcessPoolExecutor() as executor:
        # Submit tasks to test each obstruction position
        futures = {executor.submit(test_obstruction, data, start_pos, start_dir, pos): pos for pos in valid_positions}
        for future in as_completed(futures):
            result = future.result()
            if result:
                blocks.add(result)

    return blocks

if __name__ == '__main__':
    import time

    # Main logic
    start_time = time.perf_counter()

    with open("day6.txt") as f:
        data = [list(line.strip()) for line in f]

    # Find starting position and direction
    start_pos = []
    direction = [-1, 0]
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "^":
                start_pos = [y, x]
                data[y][x] = "."  # Remove guard marker from map

    # Part 1
    visited = simulate_guard(start_pos, direction, data)
    print("The first answer is:", len(visited))

    # Part 2
    blocks = find_obstruction_positions_parallel(start_pos, direction, data)
    print("The second answer is:", len(blocks))

    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.2f} seconds")


