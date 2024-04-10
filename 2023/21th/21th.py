import sys

def get_s_pos(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                return (j,i)

def explore_grid(grid, pos_list, pos, time):
    pos_res = []

    if time == 0:
        pos_list += [(pos[0], pos[1], time)]
        return [pos]
    else:
        for p in [(0,1),(0,-1),(1,0),(-1,0)]:
            new_x = pos[0] + p[0]
            new_y = pos[1] + p[1]
            new_pos = (new_x, new_y, time-1)
            if not (new_pos in pos_list) and \
               new_x >= 0 and new_y >= 0 and \
               new_x < len(grid[0]) and new_y < len(grid) and \
               (grid[new_y][new_x] == '.' or grid[new_y][new_x] == 'S'):
                    pos_list += [new_pos]
                    pos_res += explore_grid(grid, pos_list, (new_x,new_y), time-1)
        
        return list(set(pos_res))

def explore_grid_infinite(grid, pos_list, pos, time):
    pos_res = []

    if time == 0:
        pos_list += [(pos[0], pos[1], time)]
        return [pos]
    else:
        for p in [(0,1),(0,-1),(1,0),(-1,0)]:
            new_x = (pos[0] + p[0]) % len(grid[0])
            new_y = (pos[1] + p[1]) % len(grid)
            new_pos = (new_x, new_y, time-1)
            if not (new_pos in pos_list) and \
               (grid[new_y][new_x] == '.' or grid[new_y][new_x] == 'S'):
                    pos_list += [new_pos]
                    pos_res += explore_grid_infinite(grid, pos_list, (new_x,new_y), time-1)
        
        return list(set(pos_res))

f = open(sys.argv[1], 'r')
grid = [list(l) for l in f.read().splitlines()]

# Part 1 Implementation
start_pos = get_s_pos(grid)
pos_list = []
res1 = explore_grid(grid, pos_list, start_pos, 64)

# Part 2 Implementation
# pos_list = []
# res2 = explore_grid_infinite(grid, pos_list, start_pos, 10)
# print(pos_list)
# print(res2)


# Printing Results
print(f'Number of possible end positions (Part 1): {len(res1)}')
# print(f'Number of possible end positions (Part 2): {len(res2)}')
