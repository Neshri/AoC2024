def get_gps_coords(pos):
    return pos[0] * 100 + pos[1]

def move(pos, direction, board, move_set=set()):
    y, x = pos
    if direction == "^":
        velocity = (-1, 0)
    if direction == "v":
        velocity = (1, 0)
    if direction == "<":
        velocity = (0, -1)
    if direction == ">":
        velocity = (0, 1)
    new_y = y + velocity[0]
    new_x = x + velocity[1]
    if board[new_y][new_x] == "#":
        return False
    elif board[new_y][new_x] in ["[", "]"]:
        if board[new_y][new_x] == "[":
            p1 = (new_y, new_x)
            p2 = (new_y, new_x+1)
        if board[new_y][new_x] == "]":
            p1 = (new_y, new_x-1)
            p2 = (new_y, new_x)
        if direction == "^" or direction == "v":
            m1 = move(p1, direction, board, move_set)
            if not m1:
                return False
            m2 = move(p2, direction, board, move_set)
            if not m2:
                return False
            move_set.add((y, x, new_y, new_x))
        else:    
            if direction == "<":
                m = move(p1, direction, board, move_set)
            else:
                m = move(p2, direction, board, move_set)
            if not m:
                return False
            if direction == "<":
                move_set.add((p2[0], p2[1], p1[0], p1[1]))
            else:
                move_set.add((p1[0], p1[1], p2[0], p2[1]))
            move_set.add((y, x, new_y, new_x)) 
    elif board[new_y][new_x] == "O":
        m = move((new_y, new_x), direction, board, move_set)
        if not m:
            return False
        else:
            move_set.add((y, x, new_y, new_x))
    elif board[new_y][new_x] == ".":
        move_set.add((y, x, new_y, new_x))
    return (new_y, new_x), move_set

def get_start(board):
    start = (0, 0)
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == "@":
                start = (y, x)
                break
        if start != (0, 0):
            break
    return start

def print_board(board):
    for y in range(len(board)):
        print("".join(board[y]))

with open("day15.txt") as f:
    line = f.readline().strip()
    board = []
    while line != "":
        board.append(list(line))
        line = f.readline().strip()
    instructions = []
    line = f.readline().strip()
    while line != "":
        instructions.extend(list(line))
        line = f.readline().strip()
# Save original board
og_board = []
for y in range(len(board)):
    og_board.append([])
    og_board[-1].extend(board[y])
# Find start
start = get_start(board)

pos = [start[0], start[1]]
for instr in instructions:
    m = move(pos, instr, board, set())
    if m:
        l = list(m[1])
        if instr == "^":
            l = sorted(l, key=lambda x: x[0])
            pass
        elif instr == "v":
            l = sorted(l, key=lambda x: x[0], reverse=True)
            
            pass
        elif instr == "<":
            l = sorted(l, key=lambda x: x[1])
            pass
        elif instr == ">":
            l = sorted(l, key=lambda x: x[1], reverse=True)
            pass
        for i in l:
            board[i[2]][i[3]] = board[i[0]][i[1]]
            board[i[0]][i[1]] = "."
        pos = m[0]
ans = 0
for y in range(len(board)):
    for x in range(len(board[y])):
        if board[y][x] == "O":
            ans += get_gps_coords((y, x))
print("The first answer is:", ans)
# print_board(board)
# Part 2
ans = 0
# Extend board
board = []
for y in range(len(og_board)):
    board.append([])
    for x in range(len(og_board[y])):
        if og_board[y][x] == "@":
            board[y].append("@")
            board[y].append(".")
        elif og_board[y][x] == "O":
            board[y].append("[")
            board[y].append("]")
        elif og_board[y][x] == ".":
            board[y].append(".")
            board[y].append(".")
        elif og_board[y][x] == "#":
            board[y].append("#")
            board[y].append("#")

start = get_start(board)

pos = [start[0], start[1]]
for instr in instructions:
    
    # print(instr)
    m = move(pos, instr, board, set())
    if m:
        l = list(m[1])
        if instr == "^":
            l = sorted(l, key=lambda x: x[0])
            pass
        elif instr == "v":
            l = sorted(l, key=lambda x: x[0])
            l.reverse()
            pass
        elif instr == "<":
            l = sorted(l, key=lambda x: x[1])
            pass
        elif instr == ">":
            l = sorted(l, key=lambda x: x[1])
            l.reverse()
        for i in l:
            board[i[2]][i[3]], board[i[0]][i[1]] = board[i[0]][i[1]], board[i[2]][i[3]]
        pos = m[0]
    # print_board(board)
ans = 0
for y in range(len(board)):
    for x in range(len(board[y])):
        if board[y][x] == "[":
            ans += get_gps_coords((y, x))


print("The second answer is:", ans)