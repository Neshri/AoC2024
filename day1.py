
with open("day1.txt", "r") as f:
    l1 = list()
    l2 = list()
    for x in f.readlines():
        line = [int(y.strip()) for y in x.split()]
        l1.append(line[0])
        l2.append(line[1])
l1.sort()
l2.sort()
ans = 0
for x, y in zip(l1, l2):
    ans += abs(x - y)
print("The first answer is:",ans)
d = dict()
for x in l2:
    if x in d.keys():
        d[x] += 1
    else:
        d[x] = 1
ans = 0
for x in l1:
    if x in d.keys():
        ans += x * d[x]
print("The second answer is:",ans)
