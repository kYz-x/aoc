import sys
import numpy as np

f = open(sys.argv[1], 'r')

# Getting list of lines and removing carriage returns
lines = [line for line in f.read().splitlines() if line != '']
maps = []

# Get Seeds List
seeds = list(map(int, lines.pop(0).lstrip('seeds: ').split()))

# For each mapping (7 in total)
for i in range(7):
    inters = []
    
    # Removing the name of the mapping
    lines.pop(0)
    
    # Get list of intervals
    while lines and lines[0][0].isdigit():
        inters += [tuple(map(int, lines.pop(0).split()))]

        # Rapid Check
        if len(inters[-1]) != 3:
            raise ValueError(f"Expected 3 numbers for an interval not {iter}")
        
    maps += [inters]

# for map in maps:
#     for iter in map:
#         print(iter)
#     print("")

print(seeds)  
mappings  = []
locations = []

for seed in seeds:
    mapping = [seed] 
    id      = seed

    for map in maps:
        for inter in map:
            start_d, start_s, size = inter

            # if the seed is inside the interval 
            if id >= start_s and id <= (start_s + size - 1):
                id = id - start_s + start_d
                break
        
        mapping += [id]
        
    mappings  += [mapping]
    locations += [id]

print(mappings)
print(locations)

print(f'Seed with the lowest location (Part 1): {min(locations)}')
print(f'{np.argmin(locations)}, {min(locations)}')