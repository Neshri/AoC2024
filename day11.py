import time

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
    
    def length(self):
        curr_node = self
        length = 0
        while curr_node:
            length += 1
            curr_node = curr_node.next
        return length

def blink(stones):
    curr_node = stones
    while curr_node:
        if curr_node.value == 0:
            curr_node.value = 1
        elif len(str(curr_node.value)) % 2 == 0:
            s = str(curr_node.value)
            a = int(s[:len(s)//2])
            b = int(s[len(s)//2:])
            curr_node.value = a
            tmp = curr_node.next
            curr_node.next = Node(b)
            curr_node.next.next = tmp
            curr_node = curr_node.next
        else:
            curr_node.value *= 2024
        curr_node = curr_node.next
   
def blink_with_map(stones):
    send = {}
    for k, v in stones.items():
        if k == 0:
            if 1 in send.keys():
                send[1] += v
            else:
                send[1] = v
        elif len(str(k)) % 2 == 0:
            s = str(k)
            a = int(s[:len(s)//2])
            b = int(s[len(s)//2:])
            if a in send.keys():
                send[a] += v
            else:
                send[a] = v
            if b in send.keys():
                send[b] += v
            else:
                send[b] = v
        else:
            if k * 2024 in send.keys():
                send[k * 2024] += v
            else:
                send[k * 2024] = v
    return send

start_time = time.perf_counter()
with open("day11.txt") as f:
    stones = [int(x.strip()) for x in f.readline().split(" ")]
original_stones = [x for x in stones]
root = Node(stones[0])
curr_node = root
for i in range(1, len(stones)):
    curr_node.next = Node(stones[i])
    curr_node = curr_node.next
stones = root
for i in range(25):
    blink(stones)
print("The first answer is:", stones.length())
stones = {}
for x in original_stones:
    if x in stones.keys():
        stones[x] += 1
    else:
        stones[x] = 1

for i in range(75):
    stones = blink_with_map(stones)
print("The second answer is:", sum(stones.values()))
print("Execution time:", "{:.3f}".format(time.perf_counter()-start_time), "seconds")