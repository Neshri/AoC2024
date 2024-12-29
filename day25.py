
HEIGHT = 5


def overlaps(key, lock):
    for i in range(len(key)):
        if key[i] + lock[i] > HEIGHT:
            return False
    return True

locks = []
keys = []
with open("day25.txt") as f:
    schematics = f.read().split("\n\n")
    for s in schematics:
        s = s.strip()
        is_key = True if s[0] == "." else False
        obj = []
        for line in s.split("\n"):
            line = line.strip()
            obj.append(line)
        if is_key:
            keys.append(obj)
        else:
            locks.append(obj)

for i in range(len(locks)):
    tmp_lock = []
    for col in range(len(locks[i][0])):
        count = -1
        for row in range(len(locks[i])):
            if locks[i][row][col] == "#":
                count += 1
        tmp_lock.append(count)
    locks[i] = tmp_lock
for i in range(len(keys)):
    tmp_key = []
    for col in range(len(keys[i][0])):
        count = -1
        for row in range(len(keys[i])):
            if keys[i][row][col] == "#":
                count += 1
        tmp_key.append(count)
    keys[i] = tmp_key
ans = 0
for key in keys:
    for lock in locks:
        if overlaps(key, lock):
            ans += 1

print("The FINAL answer is:", ans)