

def is_equal(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

class BitComputer:
    
    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.program = []
        self.i = 0
        self.output = []

    def _get_combo(self, n):
        if 0 <= n <= 3:
            return n
        elif n == 4:
            return self.A
        elif n == 5:
            return self.B
        elif n == 6:
            return self.C
        return False
    
    def run(self, run_once=False):
        while self.i < len(self.program):
            if self.program[self.i] == 0:
                self.i += 1
                self.A = self.A // (2**self._get_combo(self.program[self.i]))
                self.i += 1
            elif self.program[self.i] == 1:
                self.i += 1
                self.B = self.B ^ self.program[self.i]
                self.i += 1
            elif self.program[self.i] == 2:
                self.i += 1
                self.B = self._get_combo(self.program[self.i]) % 8
                self.i += 1
            elif self.program[self.i] == 3:
                self.i += 1
                if self.A != 0:
                    self.i = self.program[self.i]
                    continue
                self.i += 1
            elif self.program[self.i] == 4:
                self.i += 1
                self.B = self.B ^ self.C
                self.i += 1
            elif self.program[self.i] == 5:
                self.i += 1
                tmp = self._get_combo(self.program[self.i]) % 8
                self.output.append(tmp)
                self.i += 1
                if run_once:
                    return
            elif self.program[self.i] == 6:
                self.i += 1
                self.B = self.A // (2**self._get_combo(self.program[self.i]))
                self.i += 1
            elif self.program[self.i] == 7:
                self.i += 1
                self.C = self.A // (2**self._get_combo(self.program[self.i]))
                self.i += 1
    
    def print_output(self):
        print(",".join([str(x) for x in self.output]))

    def reset(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.i = 0
        self.output = []
        
    def __repr__(self):
        return f"Register A: {self.A}, Register B: {self.B}, Register C: {self.C}, Program: {self.program}"
    
computer = BitComputer()
with open("day17.txt") as f:
    for line in f.readlines():
        line = line.strip()
        if "Register A" in line:
            n = int(line.split(": ")[1])
            computer.A = n
        if "Register B" in line:
            n = int(line.split(": ")[1])
            computer.B = n
        if "Register C" in line:
            n = int(line.split(": ")[1])
            computer.C = n
        if "Program" in line:
            n =[int(x) for x in line.split(": ")[1].split(",")]
            computer.program = n
computer.run()
print("The first answer is:")
computer.print_output()
print()

# Part 2
# 2,4,1,3,7,5,0,3,1,5,4,1,5,5,3,0

# 2,4
# B = A % 8
# Take the last 3 bits of A and store them in B
# B gets reset here

# 1,3
# B = B ^ 3
# B xor 11

# 7,5
# C = A // 2**B
# C = A with the last B(is max 7) bits removed
# C gets reset here

# 0,3
# A = A // 8 # A is only changed here
# A gets divided by 8 each run until 0 where the program exits
# program has length 16 meaning we need number of at most 8**16(48bits), at least 46 bits
# Similar to bitshift >> 3

# 1,5
# B = B ^ 5
# B xor 101
# B is always 3 bits here

# 4,1
# B = B ^ C
# B xor C

# 5,5
# OUT: B % 8
# print the last 3 bits of B
# B has to end with the same value as the program

# 3,0
# if A != 0: jump to 0
# Exits if A == 0
# the program will always jump to the same spot and thus remain consistent

ans = {}
for j in range(len(computer.program)-1, -1, -1):
    
    for i in range(1024):
        computer.reset()
        computer.A = i
        computer.run(True)
        if computer.output[0] == computer.program[j]:
            if j in ans.keys():
                ans[j].append(i)
            else:
                ans[j]= [i]
            




def build_binary_string(keys, candidates, current_key=0, current_binary="", chosen_numbers=[]):
    """
    Recursively build the 48-bit binary string using candidates that satisfy conditions for each key.

    Args:
        keys (list): List of program keys to process.
        candidates (dict): Dictionary of valid numbers for each key.
        current_key (int): The current key index being processed.
        current_binary (str): The binary string built so far.
        chosen_numbers (list): Numbers chosen so far.

    Returns:
        tuple or None: Final binary string and list of chosen numbers, or None if no solution.
    """
    # Base case: all keys processed, ensure full 48-bit binary string
    if current_key == len(keys):
        if len(current_binary) == 48:
            return current_binary, chosen_numbers
        return None

    # Fetch sorted candidates for the current key
    current_candidates = sorted(candidates[keys[current_key]])

    for number in current_candidates:
        # Convert candidate number to 7-bit binary
        binary_candidate = bin(number)[2:].zfill(10)
        # Determine the portion of current_binary to compare
        check_length = min(len(current_binary), 7)
        if check_length != 0 and binary_candidate[-check_length-3:-3] != current_binary[-check_length:]:
            continue  # Skip candidate if it doesn't align

        # Append the 3 least significant bits of the candidate
        new_binary = current_binary + binary_candidate[-3:]

        # Recur to process the next key
        result = build_binary_string(
            keys, candidates, current_key + 1, new_binary, chosen_numbers + [number]
        )
        if result:  # If a valid result is found, return it
            return result

    return None  # Backtrack if no candidates work for this key


# Prepare keys in reverse order
program_keys = list(range(len(computer.program) - 1, -1, -1))

# Run the recursive solution
solution = build_binary_string(program_keys, ans)

# Print the result
if solution:
    final_binary_string, chosen_numbers = solution
    print("Final 48-bit binary string:", final_binary_string)
    print("Numbers used:", chosen_numbers)
else:
    print("No valid solution found.")

solution = int(final_binary_string, 2)
print("The second answer is:", solution)

