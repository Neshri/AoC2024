from collections import deque
REGION_SIZE = (101, 103)
NUMBER_OF_SECONDS = 100

def calculate_safety(bots):
    q1, q2, q3, q4 = 0, 0, 0, 0
    for bot in bots.keys():
        if bot[0] < REGION_SIZE[0] // 2:
            if bot[1] < REGION_SIZE[1] // 2:
                q1 += bots[bot]
            elif bot[1] > REGION_SIZE[1] // 2:
                q3 += bots[bot]
        elif bot[0] > REGION_SIZE[0] // 2:
            if bot[1] < REGION_SIZE[1] // 2:
                q2 += bots[bot]
            elif bot[1] > REGION_SIZE[1] // 2:
                q4 += bots[bot]
    return q1 * q2 * q3 * q4

def simulate_bots(bot_list, seconds):
    bots = {}
    for bot in bot_list:
        new_px = (bot[0] + bot[2] * seconds) % REGION_SIZE[0]
        new_py = (bot[1] + bot[3] * seconds) % REGION_SIZE[1]
        if (new_px, new_py) not in bots.keys():
            bots[(new_px, new_py)] = 1
        else:
            bots[(new_px, new_py)] += 1
    return bots

def print_bots(bots):
    for y in range(REGION_SIZE[1]):
        for x in range(REGION_SIZE[0]):
            if (x, y) in bots.keys():
                print("#", end="")
            else:
                print(".", end="")
        print()

def write_bots_to_file(bots, id, filename):
    with open(filename, 'a') as f:
        f.write("\n\n")
        f.write(str(id) + "\n")
        for y in range(REGION_SIZE[1]):
            for x in range(REGION_SIZE[0]):
                if (x, y) in bots.keys():
                    f.write("#")
                else:
                    f.write(".")
            f.write("\n")

def find_longest_bot_chains(bots):
    visited = set()
    max_chain = 0
    for bot in bots.keys():
        if bot not in visited:
            chain = 0
            queue = deque()
            queue.append(bot)
            visited.add(bot)
            while queue:
                current_bot = queue.popleft()
                chain += 1
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        new_bot = (current_bot[0] + dx, current_bot[1] + dy)
                        if new_bot in bots.keys() and new_bot not in visited and new_bot != bot:
                            queue.append(new_bot)
                            visited.add(new_bot)
            if chain > max_chain:
                max_chain = chain
    return max_chain

with open("day14.txt") as f:
    data = [x.strip() for x in f.readlines()]
bot_list = []
for line in data:
    line = line.split(" ")
    p = line[0].split("=")[1].split(",")
    px = int(p[0])
    py = int(p[1])
    v = line[1].split("=")[1].split(",")
    vx = int(v[0])
    vy = int(v[1])
    bot_list.append((px, py, vx, vy))
    
print("The first answer is:", calculate_safety(simulate_bots(bot_list, NUMBER_OF_SECONDS)))

for i in range(10000):
    bots = simulate_bots(bot_list, i)
    # print(i, find_longest_bot_chains(bots))
    if find_longest_bot_chains(bots) > 100:
        write_bots_to_file(simulate_bots(bot_list, i), str(i), "bots.txt")

print("The second answer is:", 8053)
