from collections import deque
from heapq import heappush, heappop
import time

def is_valid(maze, y, x):
    return 0 <= y < len(maze) and 0 <= x < len(maze[0]) and maze[y][x] != "#"

def get_angle(d1, d2):
    if d1 == d2:
        return 0
    clockwise = (d1[0] == -d2[1] and d1[1] == d2[0])
    counterclockwise = (d1[0] == d2[1] and d1[1] == -d2[0])
    return 1 if clockwise or counterclockwise else 2


def get_cheapest_path(maze, start, end):
    visited = set()
    pq = [(0, start, (0, 1))]
    visited.add(start)
    while pq:
        cost, pos, direction = heappop(pq)
        y, x = pos
        if (y, x) == end:
            return cost
        moves = []
        if is_valid(maze, y-1, x) and (y-1, x) not in visited:
            N_cost = cost + 1 + get_angle(direction, (-1, 0))*1000
            moves.append(((y-1, x), (-1, 0), N_cost))
        if is_valid(maze, y+1, x) and (y+1, x) not in visited:
            S_cost = cost + 1 + get_angle(direction, (1, 0))*1000
            moves.append(((y+1, x), (1, 0), S_cost))
        if is_valid(maze, y, x-1) and (y, x-1) not in visited:
            W_cost = cost + 1 + get_angle(direction, (0, -1))*1000
            moves.append(((y, x-1), (0, -1), W_cost))
        if is_valid(maze, y, x+1) and (y, x+1) not in visited:
            E_cost = cost + 1 + get_angle(direction, (0, 1))*1000
            moves.append(((y, x+1), (0, 1), E_cost))
        moves = sorted(moves, key=lambda x: x[2])
        for move in moves:
            heappush(pq, (move[2], move[0], move[1]))
            visited.add(move[0])


def get_best_tiles(maze, start, end, cheapest_cost):
    def is_loeq(visited, posd, cost):
        return posd not in visited or cost <= visited[posd]

    best_tiles = set()
    queue = [(0, start, (0, 1), {start})]
    visited = {}

    while queue:
        cost, pos, direction, path = heappop(queue)
        y, x = pos

        if (y, x) == end and cost <= cheapest_cost:
            best_tiles |= path
            continue

        if pos in visited and visited[(y, x, direction[0], direction[1])] < cost:
            continue

        visited[(y, x, direction[0], direction[1])] = cost

        moves = []
        for dy, dx, ndir in [(-1, 0, (-1, 0)), (1, 0, (1, 0)), (0, -1, (0, -1)), (0, 1, (0, 1))]:
            ny, nx = y + dy, x + dx
            if is_valid(maze, ny, nx):
                move_cost = cost + 1 + get_angle(direction, ndir) * 1000
                if is_loeq(visited, (ny, nx, ndir[0], ndir[1]), move_cost):
                    moves.append(((ny, nx), ndir, move_cost))

        for move in moves:
            new_path = path | {move[0]}
            if move[2] <= cheapest_cost:
                heappush(queue, (move[2], move[0], move[1], new_path))

    return best_tiles


def get_start_and_end(maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == "S":
                start = (y, x)
            if maze[y][x] == "E":
                end = (y, x)
    return start, end

def print_combined_paths(maze, path):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if (y, x) in path:
                print("O", end="")
            else:
                print(maze[y][x], end="")
        print()


start_time = time.perf_counter()
with open("day16.txt") as f:
    maze = [list(x.strip()) for x in f.readlines()]
start, end = get_start_and_end(maze)
cheapest_cost = get_cheapest_path(maze, start, end)
print("The first answer is:", cheapest_cost)
best_tiles = get_best_tiles(maze, start, end, cheapest_cost)
print_combined_paths(maze, best_tiles)
print("The second answer is:", len(best_tiles))
print("Execution time:", "{:.3f}".format(time.perf_counter()-start_time), "seconds")
