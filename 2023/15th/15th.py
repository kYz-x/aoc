import sys
import re

# File Preprocessing
f = open(sys.argv[1], 'r')
seq = f.read().splitlines()
seq = ''.join(seq)
seq = seq.split(',')

def hash(s):
    val = 0
    for c in s:
        val = ((val + ord(c)) * 17) % 256
    return val

# Part 1 Implementation
res1 = []
for s in seq:
    res1.append(hash(s))
    
# Part 2 Implementation
boxes = [[] for _ in range(256)]
for s in seq:
    match = re.match('([a-z]+)([-=])([1-9]?)', s)
    if match:
        label = match.group(1)
        op    = match.group(2)
        num   = match.group(3)
    else:
        Exception('input sequence not valid')
        
    box_id = hash(label)
    
    if op == '=':
        found = False
        for lens in boxes[box_id]:
            if lens[0] == label:
                found = True
                lens[1] = int(num)
        if not found:
            boxes[box_id].append([label,int(num)])    
            
    elif op == '-':
        box = boxes[box_id]
        for i in range(len(box)):
            if box[i][0] == label:
                box.pop(i)
                break    
    else:
        Exception('operator not valid')
        
# Compute Score for Part 2
res2 = []
for box_i, box in enumerate(boxes):
    for lens_i, lens in enumerate(box):
        res2.append((box_i+1) * (lens_i+1) * lens[1])

# Printing Results
print(f"Sum of all HASH of the sequence (Part 1): {sum(res1)}")
print(f"Focusing power of lens configuration (Part 2): {sum(res2)}")