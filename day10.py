from collections import deque
import time

def trailhead_score(y, x, board):
    if board[y][x] != 0:
        return 0
    queue = deque()
    queue.append((y, x))
    visited = set()
    visited.add((y, x))
    score = 0
    while queue:
        y, x = queue.popleft()
        n = board[y][x]
        if n == 9:
            score += 1
        if y > 0 and board[y-1][x] == n + 1 and (y-1, x) not in visited:
            queue.append((y-1, x))
            visited.add((y-1, x))
        if y < len(board)-1 and board[y+1][x] == n + 1 and (y+1, x) not in visited:
            queue.append((y+1, x))
            visited.add((y+1, x))
        if x > 0 and board[y][x-1] == n + 1 and (y, x-1) not in visited:
            queue.append((y, x-1))
            visited.add((y, x-1))
        if x < len(board[0])-1 and board[y][x+1] == n + 1 and (y, x+1) not in visited:
            queue.append((y, x+1))
            visited.add((y, x+1))
    return score

def calculate_rating(y, x, board):
    if board[y][x] != 0:
        return 0
    queue = deque()
    queue.append((y, x))
    rating = 0
    while queue:
        y, x = queue.popleft()
        n = board[y][x]
        if n == 9:
            rating += 1
        if y > 0 and board[y-1][x] == n + 1:
            queue.append((y-1, x))
        if y < len(board)-1 and board[y+1][x] == n + 1:
            queue.append((y+1, x))
        if x > 0 and board[y][x-1] == n + 1:
            queue.append((y, x-1))
        if x < len(board[0])-1 and board[y][x+1] == n + 1:
            queue.append((y, x+1))
    return rating

start_time = time.perf_counter()
with open("day10.txt") as f:
    data = [list(x.strip()) for x in f.readlines()]
for i in range(len(data)):
    data[i] = [int(x) for x in data[i]]
ans = 0
trailheads = set()
for y in range(len(data)):
    for x in range(len(data[0])):
        if data[y][x] == 0:
            trailheads.add((y, x))
        ans += trailhead_score(y, x, data)
print("The first answer is:", ans)

ans = 0
for trailhead in trailheads:
    ans += calculate_rating(trailhead[0], trailhead[1], data)
print("The second answer is:", ans)
print("Execution time:", "{:.3f}".format(time.perf_counter()-start_time), "seconds")