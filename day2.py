
with open("day2.txt", "r") as f:
    data = [[int(y.strip()) for y in x.split()] for x in f.readlines()]

ans = 0
for l in data:
    safe = True
    if l[0] < l[1]:
        for i in range(len(l)-1):
            if l[i] >= l[i+1] or abs(l[i] - l[i+1]) > 3:
                safe = False
                break
    elif l[0] > l[1]:
        for i in range(len(l)-1):
            if l[i] <= l[i+1] or abs(l[i] - l[i+1]) > 3:
                safe = False
                break
    else:
        continue
    if safe:
        ans += 1
print("The first answer is:",ans)

def count_flaws(l):
    if len(l) < 3:
        ans += 1
        return -1
    change_list = []
    flaws = 0
    up, down = 0, 0
    for i in range(len(l)-1):
        change = l[i+1] - l[i]
        change_list.append(change)
        if change > 0:
            up += 1
        elif change < 0:
            down += 1
    change_direction = 1 if up > down else -1
    # print(change_list, change_direction)
    for i in range(len(change_list)):
        if not (0 < change_list[i] * change_direction < 4):
            flaws += 1
            if flaws > 1:
                return flaws
            if i == 0:
                if not (0 < change_list[i+1] * change_direction < 4):
                    change_list[i+1] += change_list[i]
            elif i + 1 < len(change_list):
                change_list[i+1] += change_list[i]
    # print(l, change_list, flaws)
    return flaws


ans = 0
for l in data:
    flaws = count_flaws(l)  
    if flaws < 2:
        ans += 1

print("The second answer is:",ans)



