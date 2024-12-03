import re
with open("day3.txt", "r") as f:
    data = f.readlines()
ans = 0
for line in data:
    mults = re.findall(r"mul\(\d+,\d+\)", line)
    for x in mults:
        numbers = [int(y) for y in re.findall(r"\d+", x)]
        ans += numbers[0] * numbers[1]
print("The first answer is:",ans)

ans = 0
enabled = True
for line in data:
    mults = re.findall(r"mul\(\d+,\d+\)||do\(\)||don't\(\)", line)
    for x in mults:
        numbers = [int(y) for y in re.findall(r"\d+", x)]
        if numbers and enabled:
            ans += numbers[0] * numbers[1]
        elif x == "don't()":
            enabled = False
        elif x == "do()":
            enabled = True
print("The second answer is:",ans)