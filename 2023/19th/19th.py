import sys
import re

workflow = {}
inputs   = []

def exec_cond(cond, input):
    if cond['op'] == '<':
        return input[cond['var']] < cond['val']
    elif cond['op'] == '>':
        return input[cond['var']] > cond['val']
    else: 
        raise Exception('error')

log = open('log.txt', 'w')
def exec_work(work, input):
    state = None    
    for cond in work[0]:
        log.write(str(cond) + '\n')
        if exec_cond(cond, input):
            state = cond['goto']
            break
    if not state:
        state = work[1]
        log.write(state + '\n')
    if not state:
        raise Exception('error')
    log.write(state + '\n')
    return state

# File Parsing
f = open(sys.argv[1], 'r')
lines = f.read().splitlines()
for i in range(len(lines)-1, -1, -1):
    if not lines[i]:
        inputs_str = lines[i+1:]
        works_str = lines[:i]
        break
for w in works_str:
    m1 = re.match(r"(\w+)\{.*,(\w+)\}",w)
    m2 = re.findall(r'(\w)([<>])(\d+):(\w+)', w)
    condlist = []
    for subwork in m2:
        cond = {}
        cond['var'] = subwork[0]
        cond['op']  = subwork[1]
        cond['val'] = int(subwork[2])
        cond['goto'] = subwork[3]
        condlist.append(cond)
    workflow[m1.groups(1)[0]] = (condlist, m1.groups(1)[1])
for l in inputs_str:
    m = re.findall(r'(\w)=(\d+)', l)
    input = {}
    for i in m:
        input[i[0]] = int(i[1])
    inputs.append(input)

# Part 1 Implementation
res1 = []
for input in inputs:
    state = 'in'
    while state != 'R' and state != 'A':
        state = exec_work(workflow[state], input)
    if state == 'A':
        res1.append(sum(input.values()))

# Part 2 Implementation

# Printing Results
print(f'Result from all accepted parts (Part 1): {sum(res1)}')