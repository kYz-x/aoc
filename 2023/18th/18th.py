import sys
import math

dir  = {'R': (1,0), 'D': (0,1), 'L': (-1,0), 'U': (0,-1)}

def shoelace(path):
    area = 0
    peri = 0

    for i in range(len(path)-1):
        area += path[i][0] * path[i+1][1] - path[i+1][0] * path[i][1]
        peri += math.sqrt((path[i][0] - path[i+1][0])**2 + (path[i][1] - path[i+1][1])**2)
    
    return int(abs(area)/2 + (peri/2) + 1)

# File Parsing
f = open(sys.argv[1], 'r')
lines = [l.split(' ') for l in f.read().splitlines()]

# Part 1 Implementation
path = [(0,0)]
for l in lines:
    path.append((path[-1][0] + dir[l[0]][0] * int(l[1]), path[-1][1] + dir[l[0]][1] * int(l[1])))
res1 = shoelace(path)

# Part 2 Implementation
path = [(0,0)]
for l in lines:
    dist = int(l[2][2:-2],16)
    dirr = list(dir.values())[int(l[2][-2])]
    path.append((path[-1][0] + dirr[0] * dist, path[-1][1] + dirr[1] * dist))
res2 = shoelace(path)

# Printing Results
print(f"Cubic meter capacity (Part 1): {res1}")
print(f"Cubic meter capacity (Part 2): {res2}")