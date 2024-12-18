from collections import deque

def get_shortest_path(start, end, corruptions):
    queue = deque([(start, 0)])
    visited = set([start])
    
    while queue:
        (x, y), dist = queue.popleft()
        
        if (x, y) == end:
            return dist
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            
            if ((nx, ny) not in corruptions 
                and (nx, ny) not in visited
                and 0 <= nx <= end[0]
                and 0 <= ny <= end[1]):
                queue.append(((nx, ny), dist + 1))
                visited.add((nx, ny))
                
    return -1  # no path found

with open("day18.txt") as f:
    data = [x.strip() for x in f.readlines()]
for i in range(len(data)):
    line = [int(x) for x in data[i].split(",")]
    data[i] = line


start = (0, 0)
end = (70, 70)
corruptions = set()
for i in range(1024):
    corruptions.add(tuple(data[i]))
print("The first answer is:", get_shortest_path(start, end, corruptions))

# Part two
for i in range(1024, len(data)):
    corruptions.add(tuple(data[i]))
    sp = get_shortest_path(start, end, corruptions)
    if sp == -1:
        print("The second answer is:", str(data[i][0])+","+str(data[i][1]))
        break