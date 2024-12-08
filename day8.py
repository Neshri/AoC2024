import math
from multiprocessing import Pool
import time
def calculate_new_points(p1, p2):
    # Calculate the vector from p1 to p2
    vector = (p2[0] - p1[0], p2[1] - p1[1])
    # Scale the vector by a factor of 2
    scaled_vector = (vector[0] * 2, vector[1] * 2)
    # Calculate the new points
    new_point1 = (p1[0] + scaled_vector[0], p1[1] + scaled_vector[1])
    new_point2 = (p2[0] - scaled_vector[0], p2[1] - scaled_vector[1])
    return new_point1, new_point2

def get_line_vector(p1, p2):
    # Calculate the vector from p1 to p2
    vector = (p2[0] - p1[0], p2[1] - p1[1])
    div = math.gcd(vector[0], vector[1])
    vector = (vector[0] // div, vector[1] // div)
    return vector
    

def inside(p, board):
    return 0 <= p[0] < len(board) and 0 <= p[1] < len(board[0])

def process_frequency(points):
    """
    Process the points and return a set of antinodes.

    Given a list of points, calculate all the antinodes that is within the board.

    :param points: A list of (x,y) tuples representing the points.
    :return: A set of (x,y) tuples representing the antinodes.
    """
    antinodes = set()
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            # Calculate the vector between the two points
            vector = get_line_vector(points[i], points[j])
            # Calculate the antinodes in both directions from the line
            current_point = points[i]
            while inside(current_point, board):
                # Add the current point to the antinodes set
                antinodes.add(current_point)
                # Move to the next point in the direction of the vector
                current_point = (current_point[0] + vector[0], current_point[1] + vector[1])
            current_point = points[i]
            while inside(current_point, board):
                # Add the current point to the antinodes set
                antinodes.add(current_point)
                # Move to the next point in the opposite direction of the vector
                current_point = (current_point[0] - vector[0], current_point[1] - vector[1])
    return antinodes

t = time.perf_counter()
# Read and format the board
with open("day8.txt") as f:
    board = [list(x.strip()) for x in f.readlines()]
antennas = {}
for y in range(len(board)):
    for x in range(len(board[0])):
        if board[y][x] != '.':
            if board[y][x] not in antennas.keys():
                antennas[board[y][x]] = [(y,x)]
            else:
                antennas[board[y][x]].append((y,x))

if __name__ == '__main__':
    # Part 1
    antinodes = set()
    for k in antennas.keys():
        points = antennas[k]
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                new_points = calculate_new_points(points[i], points[j])
                if inside(new_points[0], board):
                    antinodes.add(new_points[0])
                if inside(new_points[1], board):
                    antinodes.add(new_points[1])
    print("The first answer is:", len(antinodes))
    # Part 2
    with Pool(10) as p:
        antinodes = p.map(process_frequency, [antennas[k] for k in antennas.keys()])
    antinodes = set.union(*antinodes)
    print("The second answer is:", len(antinodes))
    print("Execution time:", "{:.3f}".format(time.perf_counter()-t), "seconds")