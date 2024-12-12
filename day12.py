from collections import deque

def get_area_and_perimeter(y, x, board, unclaimed):
    plant = board[y][x]
    area = 0
    perimeter = 0
    queue = deque()
    queue.append((y, x))
    garden = set()
    while queue:
        y, x = queue.popleft()
        garden.add((y, x))
        area += 1
        if y > 0 and board[y-1][x] == plant:
            if (y-1, x) in unclaimed:
                unclaimed.remove((y-1, x))
                queue.append((y-1, x))
        else:
            perimeter += 1
        if y < len(board)-1 and board[y+1][x] == plant:
            if (y+1, x) in unclaimed:
                unclaimed.remove((y+1, x))
                queue.append((y+1, x))
        else:
            perimeter += 1
        if x > 0 and board[y][x-1] == plant:
            if (y, x-1) in unclaimed:
                unclaimed.remove((y, x-1))
                queue.append((y, x-1))
        else:
            perimeter += 1
        if x < len(board[0])-1 and board[y][x+1] == plant:
            if (y, x+1) in unclaimed:
                unclaimed.remove((y, x+1))
                queue.append((y, x+1))
        else:
            perimeter += 1
    return (area, perimeter, garden)

with open("day12.txt") as f:
    board = [list(x.strip()) for x in f.readlines()]
unclaimed = set()
for y in range(len(board)):
    for x in range(len(board[0])):
        unclaimed.add((y, x))
ans = 0
garden_plots = []
while unclaimed:
    curr_y, curr_x = unclaimed.pop()
    plant = board[curr_y][curr_x]
    area, perimeter, garden = get_area_and_perimeter(curr_y, curr_x, board, unclaimed)
    garden_plots.append((garden, area))
    ans += area * perimeter
print("The first answer is:", ans)
ans = 0
for garden in garden_plots:
    garden, area = garden
    sides = 0
    min_y = min(garden, key=lambda x: x[0])[0]
    max_y = max(garden, key=lambda x: x[0])[0]
    min_x = min(garden, key=lambda x: x[1])[1]
    max_x = max(garden, key=lambda x: x[1])[1]
    for y in range(min_y, max_y+1):
        upper = False
        lower = False
        for x in range(min_x, max_x+1):
            if (y, x) in garden:
                if (y-1, x) not in garden:
                    upper = True
                elif upper:
                    sides += 1
                    upper = False
                if (y+1, x) not in garden:
                    lower = True
                elif lower:
                    sides += 1
                    lower = False
            else:
                if upper:
                    sides += 1
                    upper = False
                if lower:
                    sides += 1
                    lower = False
        if upper:
            sides += 1
        if lower:
            sides += 1
    
    for x in range(min_x, max_x+1):
        left = False
        right = False
        for y in range(min_y, max_y+1):
            if (y, x) in garden:
                if (y, x-1) not in garden:
                    left = True
                elif left:
                    sides += 1
                    left = False
                if (y, x+1) not in garden:
                    right = True
                elif right:
                    sides += 1
                    right = False
            else:
                if left:
                    sides += 1
                    left = False
                if right:
                    sides += 1
                    right = False
        if left:
            sides += 1
        if right:
            sides += 1
    ans += area * sides
print("The second answer is:", ans)
