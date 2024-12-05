rules = {}
updates = []
with open("day5.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        # First section
        if "|" in line:
            n = [int(x) for x in line.split("|")]
            if rules.get(n[0]):
                rules[n[0]].add(n[1])
            else:
                rules[n[0]] = set([n[1]])
                
        # Second section
        elif "," in line:
            n = [int(x) for x in line.split(",")]
            updates.append(n)
broken_updates = []
# Part one
ans = 0
for updt in updates:
    valid = True
    for i in range(len(updt)):
        if rules.get(updt[i]):
            for j in range(0, i):
                if updt[j] in rules[updt[i]]:
                    valid = False
                    broken_updates.append(updt)
                    break
            if not valid:
                break
    if valid:
        ans += updt[len(updt)//2]

print("The first answer is:", ans)
def flip(l, index_a, index_b):
    l[index_a], l[index_b] = l[index_b], l[index_a]

# Part two
ans = 0
for updt in broken_updates:
    # Keep swapping until no more violations exist
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(updt):
            j = i + 1
            while j < len(updt):
                # Check if we need to swap these elements
                if updt[i] in rules.keys() and updt[j] in rules[updt[i]]:
                    flip(updt, i, j)
                    changed = True
                j += 1
            i += 1
    
    # Add the middle element after sorting
    ans += updt[len(updt)//2]

print("The second answer is:", ans)
