import sys
import re

f = open(sys.argv[1], 'r')
lines = [line for line in f.read().splitlines() if line != '']

way = lines[0]
start = None
start_p2 = []

Nodes = {}

# Parsing and creating 
for line in lines[1:]:
    match = re.match('([A-Z0-9]+)\s*=\s*\(([A-Z0-9]+),\s*([A-Z0-9]+)\)', line)
    
    if not match:
        raise ValueError("Need to find exactly 'Node = (Left, Right)' synthax")

    node  = match.group(1)
    left  = match.group(2)
    right = match.group(3)

    Nodes[node] = (left, right)

    if not start:
        start = node

    if node[-1] == 'A':
        start_p2 += [node]


### Part 1 Implementation ###
node = start
step = 0

while node != 'ZZZ':
    for dir in way:
        node  = Nodes[node][0] if dir == 'L' else Nodes[node][1]
        step += 1

print(f"Number of step required to reach ZZZ (Part 1): {step}")

### Part 2 Implementation ###
step = 0
end_p2 = []

# True if all node names finish by 'Z'
def isEnd(end_nodes):
    if not end_nodes:
        return False

    for node in end_nodes:
        if node[-1] != 'Z':
            return False
    return True

while not isEnd(end_p2):
    end_p2 = []
    for start in start_p2:
        node = start
        for dir in way:
            node  = Nodes[node][0] if dir == 'L' else Nodes[node][1]
        end_p2 += [node] 
    
    start_p2 = end_p2
    step += len(way)

print(f'Number of step required to reach xxZ (Part 2): {step}')
    
