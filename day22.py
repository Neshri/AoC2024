import time
from collections import deque


# Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
# Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. 
# Then, mix this result into the secret number. Finally, prune the secret number.
# Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.


# To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number. 
# Then, the secret number becomes the result of that operation. 
# (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)

# To prune the secret number, calculate the value of the secret number modulo 16777216. 
# Then, the secret number becomes the result of that operation. 
# (If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.)
memory = {}

def prune(secret_number):
    return secret_number % 16777216

def mix(secret_number, n):
    return secret_number ^ n

def get_monkey_number(secret_number, n):
    banana_diff = deque()
    used_keys = set()
    for i in range(n):
        last = secret_number
        
        # Calculate the next secret number
        tmp = secret_number * 64
        secret_number = mix(secret_number, tmp)
        secret_number = prune(secret_number)
        tmp = secret_number // 32
        secret_number = mix(secret_number, tmp)
        secret_number = prune(secret_number)
        tmp = secret_number * 2048
        secret_number = mix(secret_number, tmp)
        secret_number = prune(secret_number)
        
        # Do stuff for part 2
        diff = (secret_number % 10) - (last % 10) 
        if i > 0:
            banana_diff.append(diff)
        if len(banana_diff) > 4:
            banana_diff.popleft()
        if len(banana_diff) == 4:
            end_digit = secret_number % 10
            key = tuple(banana_diff)
            if key not in used_keys:
                used_keys.add(key)
                if key in memory.keys():
                    memory[key] += end_digit
                else:
                    memory[key] = end_digit
    return secret_number

start_time = time.perf_counter()
with open("day22.txt") as f:
    initial_secrets = [int(x.strip()) for x in f.readlines()]
ans = 0
for n in initial_secrets:
    ans += get_monkey_number(n, 2000)
print("The first answer is:", ans)
ans = 0
for k, v in memory.items():
    if v > ans:
        ans = v
print("The second answer is:", ans)
print("Execution time:", "{:.3f}".format(time.perf_counter()-start_time), "seconds")