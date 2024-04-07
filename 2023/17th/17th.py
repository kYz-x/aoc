import sys
import random
import heapq
from enum import Enum

# File Parsing
f = open(sys.argv[1],'r')
grid = [list(map(int,l)) for l in f.read().splitlines()]
dir = {'n':(0 ,-1), 's':(0 , 1), 'e':(1 , 0), 'w':(-1, 0)}
odir = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

def bellman_ford(grid, source, dest):
    path = [[float('inf') for c in l] for l in grid]
    pred = [["" for c in l] for l in grid]
    path[source[1]][source[0]] = 0

    # For every vertices
    for it in range(len(grid) * len(grid[0])):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                # For all ajdacent vertices
                for d in dir.keys():
                    dj,di = dir[d]
                    
                    if (len(pred[i][j]) >= 3 and pred[i][j][-3:] == d+d+d) or \
                        len(pred[i][j]) > 0 and odir[pred[i][j][-1]] == d:
                        continue

                    if i + di >= 0 and i + di < len(grid) and \
                        j + dj >= 0 and j + dj < len(grid[i]):
                        if path[i+di][j+dj] > path[i][j] + grid[i+di][j+dj]:
                            path[i+di][j+dj] = path[i][j] + grid[i+di][j+dj]
                            pred[i+di][j+dj] = pred[i][j] + d

    print(path)
    print(pred)

    return path[dest[1]][dest[0]]

def dijkstra(grid,source,dest):
    path = [[float('inf') for c in l] for l in grid]
    pred = [["" for c in l] for l in grid]
    path[source[1]][source[0]] = 0
    q = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            q.append((i,j))
    # for i in range(5):
    #     random.shuffle(q)

    while q:
        min_path = float("inf")

        # Get the vertex that has the minimal estimated shortest path
        for idx, v in enumerate(q):
            if min_path > path[v[1]][v[0]]:
                min_path = path[v[1]][v[0]]
                min_idx  = idx
        
        j,i = q.pop(min_idx)

        for d in dir.keys():
            dj,di = dir[d]

            if (len(pred[i][j]) >= 3 and pred[i][j][-3:] == d+d+d) or \
                len(pred[i][j]) > 0 and odir[pred[i][j][-1]] == d:
                continue

            if i + di >= 0 and i + di < len(grid) and \
                j + dj >= 0 and j + dj < len(grid[i]):
                if path[i+di][j+dj] > path[i][j] + grid[i+di][j+dj]:
                    path[i+di][j+dj] = path[i][j] + grid[i+di][j+dj]
                    pred[i+di][j+dj] = pred[i][j] + d


    print(path)
    print(pred)

    return path[dest[1]][dest[0]]


def new_dijkstra(grid,source,dest):
    q = []
    seen = []
    heapq.heappush(q, (0, 0, 0,'e',0))
    heapq.heappush(q, (0, 0, 0,'s',0))

    while q:
        cost, j, i, direction, steps = heapq.heappop(q)
        pos = (j,i)

        if pos == dest:
            return cost

        if (j, i, direction, steps) in seen:
            continue
        else:
            seen.append((j, i, direction, steps))

        for d in dir.keys():
            dj,di = dir[d]

            if (steps >= 3 and d == direction) or odir[direction] == d:
                continue
            elif d == direction:
                steps = steps + 1
            else:
                steps = 1

            if i + di >= 0 and i + di < len(grid) and \
               j + dj >= 0 and j + dj < len(grid[i]):
                heapq.heappush(q, (cost + grid[i+di][j+dj], j+dj, i+di, d, steps))


source = (0,0)
dest   = (len(grid[0])-1, len(grid)-1)

# Part 1 Implementation
res1 = new_dijkstra(grid,source,dest)

# Part 2 Implementation

# Printing Result
print(f'Minimum total heal loss (Part 1): {res1}')
