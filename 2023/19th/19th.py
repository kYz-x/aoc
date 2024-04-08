import sys
import re

workflow = {}
inputs   = []
encoding = {'x':0, 'm':1, 'a':2, 's':3}


def exec_cond(cond, input):
    if cond['op'] == '<':
        return input[cond['var']] < cond['val']
    elif cond['op'] == '>':
        return input[cond['var']] > cond['val']

def exec_work(work, input):
    state = None    
    for cond in work[0]:
        if exec_cond(cond, input):
            state = cond['goto']
            break
    if not state:
        state = work[1]
    return state

def explore_workflow(works, state, range):
    next_range = range
    a_ranges = []

    # End condition for recursion   
    if state == 'A':
        return [range]
    elif state == 'R':
        return []

    for cond in works[state][0]:
        true_state, true_range, false_range = get_state_range(cond, next_range)
        next_range = false_range
        a_ranges += explore_workflow(works, true_state, true_range)
    
    false_state = works[state][1]
    a_ranges += explore_workflow(works, false_state, false_range)

    return a_ranges
    
def get_state_range(cond, next_range):
    true_state = cond['goto']
    true_range = next_range[:]
    false_range = next_range[:]
    r_t = [true_range[encoding[cond['var']]][0], true_range[encoding[cond['var']]][1]]
    r_f = r_t[:]

    if cond['op'] == '<':
        # True Range
        if (cond['val'] - 1) < r_t[1]: 
            r_t[1] = cond['val'] - 1
        # False Range
        if cond['val'] > r_f[0]:
            r_f[0] = cond['val']
    elif cond['op'] == '>':
        # True Range
        if cond['val'] < r_f[1]: 
            r_f[1] = cond['val']
        # False Range
        if (cond['val'] + 1) > r_t[0]:
            r_t[0] = cond['val'] + 1
    
    true_range[encoding[cond['var']]]  = (r_t[0], r_t[1])
    false_range[encoding[cond['var']]] = (r_f[0], r_f[1])

    return true_state, true_range, false_range

def compute_comb(ranges):
    comb = 0
    for r in ranges:
        comb_varr = 1
        for varr in r:
            if (varr[1] - varr[0] + 1) > 0:
                comb_varr *= varr[1] - varr[0] + 1
        comb += comb_varr
    return comb

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
ranges = explore_workflow(workflow, 'in', [(1,4000),(1,4000),(1,4000),(1,4000)])
res2   = compute_comb(ranges)

# Printing Results
print(f'Result from all accepted parts (Part 1): {sum(res1)}')
print(f'Number of accepted combinaison (Part 2): {res2}')