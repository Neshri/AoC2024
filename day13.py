class ArcadeMachine:
    def __init__(self):
        pass

    def __repr__(self):
        return f"Button A: {self.button_a}, Button B: {self.button_b}, Prize: {self.prize}"

A_PRIZE, B_PRIZE = 3, 1

# Parse machines from file
def parse_machines(filename):
    machines = []
    with open(filename) as f:
        machine = ArcadeMachine()
        for line in f.readlines():
            line = line.strip()
            if line == "":
                if machine not in machines:
                    machines.append(machine)
                machine = ArcadeMachine()
            else:
                x, y = [a.strip() for a in line.split(":")[1].split(",")]
                x = int(x.split("+")[1]) if "+" in x else int(x.split("=")[1])
                y = int(y.split("+")[1]) if "+" in y else int(y.split("=")[1])
                if "Button A" in line:
                    machine.button_a = (y, x)
                elif "Button B" in line:
                    machine.button_b = (y, x)
                else:
                    machine.prize = (y, x)
        if machine not in machines:
            machines.append(machine)
    return machines

# Calculate tokens for a set of machines
def calculate_tokens(machines, prize_offset=(0, 0)):
    tokens = 0
    for m in machines:
        a, b, p = m.button_a, m.button_b, m.prize
        p = (p[0] + prize_offset[0], p[1] + prize_offset[1])
        
        det = a[1] * b[0] - a[0] * b[1]
        if det == 0:
            continue

        i = (p[1] * b[0] - p[0] * b[1]) / det
        j = (p[1] - a[1] * i) / b[1]

        if i >= 0 and j >= 0 and i.is_integer() and j.is_integer():
            i, j = int(i), int(j)
            tokens += A_PRIZE * i + B_PRIZE * j
    return tokens

# Main execution
if __name__ == "__main__":
    machines = parse_machines("day13.txt")

    # First answer
    tokens_part1 = calculate_tokens(machines)
    print("The first answer is:", tokens_part1)

    # Second answer with prize offset
    tokens_part2 = calculate_tokens(machines, prize_offset=(10**13, 10**13))
    print("The second answer is:", tokens_part2)
