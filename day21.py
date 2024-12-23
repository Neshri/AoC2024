
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

def is_valid_path(y1, x1, y2, x2, keypad):
    """
    Check if a direct path between two points is valid (no gaps).

    Args:
        y1, x1, y2, x2 (int): Start and target coordinates.
        keypad (list): 2D list representing the keypad layout.

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    # Vertical path check
    if x1 == x2:
        step = 1 if y1 < y2 else -1
        for y in range(y1, y2 + step, step):
            if keypad[y][x1] is None:
                return False
        return True

    # Horizontal path check
    if y1 == y2:
        step = 1 if x1 < x2 else -1
        for x in range(x1, x2 + step, step):
            if keypad[y1][x] is None:
                return False
        return True

    return False

def get_shortest_path_recursive(codesequence, pos, index, built_sequence, depth, memory, numeric=True):
    """
    Compute the shortest path recursively across multiple keypad layers.

    Args:
        codesequence (str): Original code sequence to process.
        index (int): Current position in the codesequence being read.
        built_sequence (str): Sequence being constructed based on moves.
        depth (int): Current recursion depth (keypad switches).
        memory (dict): Memoization dictionary.
        numeric (bool): Whether the current keypad is numeric or directional.

    Returns:
        str: Shortest valid sequence of moves across keypads.
    """
    # Base case: Finished processing all keypads
    if depth == 0:
        return codesequence

    # Memoization key
    key = (codesequence, depth)
    if key in memory.keys():
        return memory[key]

    # Set keypad and map based on numeric flag
    keypad = KEYPAD if numeric else D_PAD
    keypad_map = KEYPAD_MAP if numeric else D_PAD_MAP

    # Base case: Reached the end of the current codesequence
    if index >= len(codesequence):
        # Recurse to the next depth level with the newly built sequence
        result = get_shortest_path_recursive(built_sequence, (0, 2), 0, "", depth - 1, memory, numeric=False)
        memory[key] = result
        return result

    # Get the current character and position
    current_char = codesequence[index]
    current_pos = keypad_map[current_char]

    # Get possible moves (xy and yx paths)
    shortest_sequence = None
    for move_order in ["xy", "yx"]:
        # Generate a valid path for the current move order
        new_sequence = generate_path_with_order(move_order, pos, current_pos, numeric)
        if new_sequence is not None:
            # Recurse with the updated index and sequence
            result = get_shortest_path_recursive(codesequence, current_pos, index + 1, built_sequence + new_sequence + "A", depth, memory, numeric)
            # Compare and keep the shortest valid result
            if shortest_sequence is None or len(result) < len(shortest_sequence):
                shortest_sequence = result
    # if index == len(codesequence) - 1:
    #     # Memoize the completed sequence for this depth
    #     if key in memory.keys():
    #         if len(shortest_sequence) < len(memory[key]):
    #             memory[key] = shortest_sequence
    #     else:
    #         memory[key] = shortest_sequence
    return shortest_sequence


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
    # Same implementation as before
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



# Input and Keypad definitions
with open("day21.txt") as f:
    codes = [x.strip() for x in f.readlines()]


start_positions = {
    "numeric": (3, 2),  # Numeric keypad starts at "A"
    "directional": (0, 2)  # Directional keypads start at "A"
}

total_complexity = 0

memory = {}
# Processing codes
for code in codes:
    final_path = get_shortest_path_recursive(code, start_positions["numeric"], 0, "", 3, memory, True)
    final_path_length = len(final_path)
    
    # Calculate complexity
    numeric_part = int(code[:-1])  # Extract numeric part
    complexity = final_path_length * numeric_part
    total_complexity += complexity

    # Debugging output
    print(f"Code: {code}")
    print(f"Final directional path ({final_path_length}): {final_path}")
    print(f"Complexity: {complexity}\n")
    print(memory[(code, 3)] == final_path)

# Output total complexity
print("The first answer is:", total_complexity)
