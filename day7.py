import re
from itertools import product
import time
from multiprocessing import Pool

def check_if_possible(l):
    target = l[0]
    n = l[1:]
    ops = list(product(['*', '+'], repeat=len(n)-1))
    for op in ops:
        result = n[0]
        for i in range(len(n)-1):
            if op[i] == '*':
                result *= n[i+1]
            else:
                result += n[i+1]
        if result == target:
                return True
    return False

def check_if_possible_2(l):
    target = l[0]
    n = l[1:]
    ops = list(product(['*', '+', '||'], repeat=len(n)-1))
    for op in ops:
        result = n[0]
        for i in range(len(n)-1):
            if op[i] == '*':
                result *= n[i+1]
            elif op[i] == '||':
                result = int(str(result) + str(n[i+1]))
            else:
                result += n[i+1]
        if result == target:
                return True
    return False

if __name__ == '__main__':
    t = time.perf_counter()
    with open("day7.txt") as f:
        lines = [x.strip() for x in f.readlines()]
    data = list()
    for line in lines:
        n = [int(x) for x in re.findall(r'\d+', line)]
        data.append(n)
    ans = 0
    for line in data:
        if check_if_possible(line):
            ans += line[0]
    print("The first answer is:", ans)
    with Pool(10) as p:
        ans = 0
        result = p.map(check_if_possible_2, data)
        for i in range(len(data)):
            if result[i]:
                ans += data[i][0]
    print("The second answer is:", ans)
    print("Execution time:", "{:.3f}".format(time.perf_counter()-t), "seconds")