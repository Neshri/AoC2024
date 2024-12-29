
class Wire:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.input = None
        self.outputs = []
        self.correct_value = None

    def update(self):
        if self.input:
            self.input.execute()

    def __repr__(self):
        return f"Wire: {self.id}, Value: {self.value}"

class Gate:
    def __init__(self, op, inputs, output):
        self.op = op
        self.inputs = inputs
        self.output = output
        
    def execute(self):
        self.inputs[0].update()
        self.inputs[1].update()
        if self.op == "XOR":
            self.output.value = self.inputs[0].value ^ self.inputs[1].value
        elif self.op == "OR":
            self.output.value = self.inputs[0].value | self.inputs[1].value
        elif self.op == "AND":
            self.output.value = self.inputs[0].value & self.inputs[1].value
        
    def __repr__(self):
        return f"Gate: {self.op}, Inputs: {self.inputs}, Outputs: {self.output}"
    
def get_wires(prefix, wires):
    wanted_wires = []
    for w in wires.values():
        if w.id.startswith(prefix):
            wanted_wires.append(w)
    wanted_wires.sort(key=lambda x: x.id)
    return wanted_wires

def get_binary(prefix, wires):
    wanted_wires = []
    for w in wires.values():
        if w.id.startswith(prefix):
            wanted_wires.append(w)
    wanted_wires.sort(key=lambda x: x.id)
    send = ""
    for w in wanted_wires:
        w.update()
        send += str(w.value)
    return send[::-1]

# Parse input
with open("day24.txt") as f:
    setup = []
    while True:
        line = f.readline().strip()
        if line == "":
            break
        id, value = line.split(": ")
        value = int(value)
        setup.append([id, value])
    gates = [x.strip() for x in f.readlines()]
wires = {}
for w in setup:
    wires[w[0]] = Wire(w[0], w[1])
for i in range(len(gates)):
    g, to = gates[i].split(" -> ")
    if to not in wires.keys():
        wires[to] = Wire(to, 0)
    a, op, b = g.split(" ")
    if a not in wires.keys():
        wires[a] = Wire(a, 0)
    if b not in wires.keys():
        wires[b] = Wire(b, 0)
    gates[i] = Gate(op, [wires[a], wires[b]], wires[to])
    wires[a].outputs.append(gates[i])
    wires[b].outputs.append(gates[i])
    wires[to].input = gates[i]

# Execute network
for w in wires.values():
    w.update()
print("The first answer is:", int(get_binary("z", wires), 2))

x = int(get_binary("x", wires), 2)
y = int(get_binary("y", wires), 2)
print("X Value:", x)
print("Y Value:", y)
print("Wanted Value:", x + y)
z_wires = get_wires("z", wires)
wanted_bin = bin(x + y)[2:].zfill(len(z_wires))
print("Wanted Binary:", wanted_bin)
print("Current Binary:", get_binary("z", wires))

# Find everything that goes against the full-adder architecture
swapped_wires = set()
for g in gates:
    gin_a, gin_b = g.inputs
    op = g.op
    out = g.output

    if op == "AND":
        next_g = out.outputs
        if len(next_g) != 1 or (len(next_g) == 1 and next_g[0].op != "OR"):
            if gin_a.id not in ("x00", "y00"):
                swapped_wires.add(out.id)
    if op == "OR":
        next_g = out.outputs
        for ng in next_g:
            if ng.op == "OR":
                swapped_wires.add(out.id)
    if op == "XOR" and gin_a.id[0] not in "xy" and gin_b.id[0] not in "xy" and out.id[0] not in "z":
        swapped_wires.add(out.id)
    if op == "XOR":
        next_g = out.outputs
        for ng in next_g:
            if ng.op == "OR":
                swapped_wires.add(out.id)
    if op != "XOR" and out.id[0] == "z" and out.id != f"z{len(z_wires) - 1}":
        swapped_wires.add(out.id)

print("The second answer is:", ",".join(sorted(list(swapped_wires))))
