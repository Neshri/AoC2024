from itertools import pairwise
import time
KEYPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"]
]
KEYPAD_MAP = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2)
}
D_PAD = [
    [None, "^", "A"],
    ["<", "v", ">"]
]
D_PAD_MAP = {
    "^": (0, 1),
    "v": (1, 1),
    "<": (1, 0),
    ">": (1, 2),
    "A": (0, 2)
}


def find_shortest_path_length(code, depth):
    """Calculate exact path length through all keypad layers"""
    sequence_cache = {}
    
    def get_shortest_sequence_length(moves, remaining_depth):
        cache_key = (moves, remaining_depth)
        if cache_key in sequence_cache:
            return sequence_cache[cache_key]
        if remaining_depth == 0:
            return len(moves)
        total_cost = 0
        for c1, c2 in pairwise(f"A{moves}"):
            from_pos = D_PAD_MAP[c1]
            target_pos = D_PAD_MAP[c2]
            cost = float('inf')
            for order in ["xy", "yx"]:
                key = (c1, c2, order, remaining_depth)
                if key in sequence_cache:
                    tmp_cost = sequence_cache[key]
                else:
                    path = generate_path_with_order(order, from_pos, target_pos, numeric=False)
                    if path is None:
                        continue
                    path += "A"
                    tmp_cost = get_shortest_sequence_length(path, remaining_depth-1)
                    sequence_cache[key] = tmp_cost
                if tmp_cost < cost:
                    cost = tmp_cost
            total_cost += cost
            
        return total_cost

    # Generate initial numeric sequence
    total_cost = 0
    for c1, c2 in pairwise(f"A{code}"):
        from_pos = KEYPAD_MAP[c1]
        target_pos = KEYPAD_MAP[c2]
        cost = float('inf')
        for order in ["xy", "yx"]:
            key = (c1, c2, order, depth)
            if key in sequence_cache:
                tmp_cost = sequence_cache[key]
            else:    
                path = generate_path_with_order(order, from_pos, target_pos, numeric=True)
                if path is None:
                    continue
                path += "A"
                tmp_cost = get_shortest_sequence_length(path, depth-1)
            if tmp_cost < cost:
                cost = tmp_cost
                sequence_cache[key] = cost
        total_cost += cost
        from_pos = target_pos
    return total_cost

def generate_path_with_order(order, start_pos, target_pos, numeric):
    """
    Generate a path based on a given order ('xy' or 'yx').

    Args:
        order (str): Order to generate moves ('xy' or 'yx').
        start_pos (tuple): Starting position on the keypad.
        target_pos (tuple): Target position on the keypad.
        numeric (bool): Whether to use the numeric keypad or directional.

    Returns:
        str or None: Path sequence if valid, or None if invalid.
    """
    # Set the appropriate keypad
    keypad = KEYPAD if numeric else D_PAD

    # Determine the sequence of moves
    if order == "xy":
        intermediate_pos = (start_pos[0], target_pos[1])
        path1 = is_valid_path(start_pos[0], start_pos[1], start_pos[0], target_pos[1], keypad)
        path2 = is_valid_path(start_pos[0], target_pos[1], target_pos[0], target_pos[1], keypad)
        if path1 and path2:
            return generate_moves(start_pos, intermediate_pos) + \
                   generate_moves(intermediate_pos, target_pos)

    elif order == "yx":
        intermediate_pos = (target_pos[0], start_pos[1])
        path1 = is_valid_path(start_pos[0], start_pos[1], target_pos[0], start_pos[1], keypad)
        path2 = is_valid_path(target_pos[0], start_pos[1], target_pos[0], target_pos[1], keypad)
        if path1 and path2:
            return generate_moves(start_pos, intermediate_pos) + \
                   generate_moves(intermediate_pos, target_pos)

    # Invalid path
    return None


def is_valid_path(y1, x1, y2, x2, keypad):
    """
    Check if the path between two positions is valid.
    """
    if x1 == x2:
        step = 1 if y1 < y2 else -1
        for y in range(y1, y2 + step, step):
            if keypad[y][x1] is None:
                return False
        return True

    if y1 == y2:
        step = 1 if x1 < x2 else -1
        for x in range(x1, x2 + step, step):
            if keypad[y1][x] is None:
                return False
        return True

    return False


def generate_moves(start, end):
    """
    Generate a sequence of moves between two points.
    """
    y1, x1 = start
    y2, x2 = end
    moves = []

    if x1 != x2:  # Horizontal moves
        step = 1 if x1 < x2 else -1
        for _ in range(abs(x2 - x1)):
            moves.append(">" if step == 1 else "<")

    if y1 != y2:  # Vertical moves
        step = 1 if y1 < y2 else -1
        for _ in range(abs(y2 - y1)):
            moves.append("v" if step == 1 else "^")

    return "".join(moves)


start_time = time.perf_counter()
# Input and Keypad definitions
with open("day21.txt") as f:
    codes = [x.strip() for x in f.readlines()]
total_complexity = 0
# Processing codes
for code in codes:
    final_path_length = find_shortest_path_length(code, 3)
    
    # Calculate complexity
    numeric_part = int(code[:-1])  # Extract numeric part
    complexity = final_path_length * numeric_part
    total_complexity += complexity
# Output total complexity
print("The first answer is:", total_complexity)

total_complexity = 0
for code in codes:
    final_path_length = find_shortest_path_length(code, 26)
    # Calculate complexity
    numeric_part = int(code[:-1])  # Extract numeric part
    complexity = final_path_length * numeric_part
    total_complexity += complexity
# Output total complexity
print("The second answer is:", total_complexity)
print("Execution time:", "{:.3f}".format(time.perf_counter()-start_time), "seconds")