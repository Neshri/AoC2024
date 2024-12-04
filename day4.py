import re
import numpy as np
with open("day4.txt", "r") as f:
    data = [x.strip() for x in f.readlines()]

ans = 0
phrase = r"(?=(XMAS|SAMX))"
matrix = []
# Horizontal
for line in data:
    finds = re.findall(phrase, line)
    ans += len(finds)
    matrix.append(list(line))
d = np.array(matrix)
# Vertical
vertical = d.T
for col in vertical:
    col_str = ''.join(col)
    finds = re.findall(phrase, col_str)
    ans += len(finds)
rows, cols = d.shape
diagonals = []

# Regular diagonals (top-left to bottom-right)
# Main and above main diagonal
for k in range(cols):
    diagonal = np.diagonal(d, offset=k)
    if len(diagonal) > 0:
        diagonals.append(diagonal)

# Below main diagonal
for k in range(1, rows):
    diagonal = np.diagonal(d, offset=-k)
    if len(diagonal) > 0:
        diagonals.append(diagonal)

# Anti-diagonals (top-right to bottom-left)
flipped = np.fliplr(d)
for k in range(cols):
    diagonal = np.diagonal(flipped, offset=k)
    if len(diagonal) > 0:
        diagonals.append(diagonal)

for k in range(1, rows):
    diagonal = np.diagonal(flipped, offset=-k)
    if len(diagonal) > 0:
        diagonals.append(diagonal)
# Convert diagonals to strings and check for patterns
for diagonal in diagonals:
    diagonal_str = ''.join(diagonal)
    finds = re.findall(phrase, diagonal_str)
    ans += len(finds)
print("The first answer is:",ans)

ans = 0
for y in range(1, len(data)-1):
    for x in range(1, len(data[y])-1):
        if data[y][x] == "A":
            tl_br = "".join([data[y-1][x-1], data[y][x], data[y+1][x+1]])
            tr_bl = "".join([data[y-1][x+1], data[y][x], data[y+1][x-1]])
            if (tl_br == "SAM" or tl_br == "MAS") and (tr_bl == "SAM" or tr_bl == "MAS"):
                ans += 1

print("The second answer is:",ans)