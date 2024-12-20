from collections import deque
import time

def is_valid(y, x, board):
    return 0 <= y < len(board) and 0 <= x < len(board[0]) and board[y][x] != "#"

def get_shortest_path_to_exit(board, end):
    memo = {}  # Dictionary to store the shortest path to the exit for each position
    visited = set()
    queue = deque()
    queue.append((end, 0))  # Start BFS from the exit
    while queue:
        pos, dist = queue.popleft()
        y, x = pos
        # Memoize the shortest distance to the exit from this position
        memo[pos] = dist
        # Explore neighboring positions
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if is_valid(ny, nx, board) and (ny, nx) not in visited:
                queue.append(((ny, nx), dist + 1))
                visited.add(pos)

    return memo

def get_cheats_with_time(start, board, max_time, short_map, cheat_max_time):
    """Identify all valid cheats that reach the endpoint within max_time and save min_save time."""
    cheats = set()
    visited = set()
    queue = deque([(start, 0)])  # (current position, time so far)
    while queue:
        pos, i = queue.popleft()
        y, x = pos
        if i > max_time:
            continue
        # Cheat moves:
        for dy in range(-cheat_max_time, cheat_max_time + 1):
            for dx in range(-cheat_max_time, cheat_max_time + 1):
                if not (1 < abs(dy) + abs(dx) <= cheat_max_time):
                    continue
                ny, nx = y + dy, x + dx
                # Ensure the cheat lands on valid spaces
                if is_valid(ny, nx, board) and (ny, nx) not in visited:
                    cheat_time = i + abs(dy) + abs(dx) + short_map[(ny, nx)]
                    if cheat_time <= max_time:
                        cheats.add((y, x, ny, nx))  # Add cheat as (start, end)
        # Normal moves: One step at a time
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if is_valid(ny, nx, board) and (ny, nx) not in visited:
                queue.append(((ny, nx), i + 1))
                visited.add((ny, nx))

    return cheats


start_time = time.perf_counter()
with open("day20.txt") as f:
    data = [list(x.strip()) for x in f.readlines()]

start = (0, 0)
end = (0, 0)
for y in range(len(data)):
    for x in range(len(data[0])):
        if data[y][x] == "E":
            end = (y, x)
        if data[y][x] == "S":
            start = (y, x)
shortest = get_shortest_path_to_exit(data, end)

cheats = get_cheats_with_time(start, data, shortest[start]-100, shortest, 2)
print("The first answer is:", len(cheats))

cheats = get_cheats_with_time(start, data, shortest[start]-100, shortest, 20)
print("The second answer is:", len(cheats))

print("Execution time:", "{:.3f}".format(time.perf_counter()-start_time), "seconds")