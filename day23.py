from itertools import combinations

def is_clique(nodes, computers):
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if nodes[j] not in computers[nodes[i]]:
                return False
    return True

def three_is_connected(s, computers):
    return (s[0] in computers[s[1]] and s[0] in computers[s[2]] and s[1] in computers[s[2]])

with open("day23.txt") as f:
    data = [x.strip() for x in f.readlines()]
computers = {}
for link in data:
    a, b = link.split("-")
    # Add b to a
    if a not in computers.keys():
        computers[a] = set()
    computers[a].add(b)
    # Add a to b
    if b not in computers.keys():
        computers[b] = set()
    computers[b].add(a)
three_sets = set()
for k, v in computers.items():
    sets_of_2 = [list(set) for set in combinations(v, 2)]
    for s in sets_of_2:
        s.append(k)
        if three_is_connected(s, computers):
            three_sets.add(frozenset(s))
ans = 0
for s in three_sets:
    for id in s:
        if id[0] == "t":
            ans += 1
            break
print("The first answer is:", ans)

max_clique = []
for k, v in computers.items():
    for other_k, other_v in computers.items():
        if k != other_k and other_k in v:
            clique = [k, other_k]
            for node in v:
                if node != other_k and node in computers[other_k]:
                    clique.append(node)
            clique = list(set(clique))
            if is_clique(clique, computers) and len(clique) > len(max_clique):
                max_clique = clique

password = ','.join(sorted(max_clique))
print("The second answer is:", password)
