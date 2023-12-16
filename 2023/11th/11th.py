import sys
import copy

# Finding all galaxies coordinates
def find_galaxies(space):
    galaxies = []
    for y, line in enumerate(space):
        for x, char in enumerate(line):
            if char == '#':
                galaxies.append((x,y))
    return galaxies

def find_empty_coord(space):
    nempty_cols = []
    cols = [i for i in range(len(space[0]))]

    # Finding empty lines
    e_lines = [y for y, line in enumerate(space) if '#' not in line]
    
    # Findint Empty Columns
    for y, line in enumerate(space):
        for x, char in enumerate(line):
            if char == '#':
                nempty_cols.append(x)
    e_cols = list(set(cols) - set(nempty_cols))
    
    return (e_cols, e_lines)

def expand_space(s, times=1):
    # Init
    space = copy.deepcopy(s)
    empty_lines = []
    cols   = [i for i in range(len(space[0]))]
    nempty_cols = []

    # Finding Empty Lines 
    empty_lines = [y for y, line in enumerate(space) if '#' not in line]
    
    # Findint Empty Columns
    for y, line in enumerate(space):
        for x, char in enumerate(line):
            if char == '#':
                nempty_cols.append(x)
    empty_cols = list(set(cols) - set(nempty_cols))
    
    # Inserting Empty Lines
    for y in reversed(sorted(empty_lines)):
        for t in range(times):
            space.insert(y, ['.'] * len(space[0]))
    
    # Inserting Empty Columns
    for line in (space):
        for x in reversed(sorted(empty_cols)):
            for t in range(times):
                line.insert(x, '.')
    
    return space
    
def find_distance(coord_a, coord_b):
    return abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1]) 

def find_distance_p2(coord_a, coord_b, e_coords, times=2):
    e_cols, e_lines = e_coords
    e_spaces = [0] * 2

    for dim in range(len(coord_a)):
        start_coord = min(coord_a[dim], coord_b[dim])
        end_coord   = max(coord_a[dim], coord_b[dim])
        for coord in range(start_coord, end_coord):
            for e_coord in e_coords[dim]:
                if e_coord == coord:
                    e_spaces[dim] += 1
    
    return abs(coord_a[0] - coord_b[0]) + e_spaces[0] * (times - 1) + \
           abs(coord_a[1] - coord_b[1]) + e_spaces[1] * (times - 1)

# Main Function
def main():
    
    # Parsing File
    f = open(sys.argv[1], 'r')
    space = [list(line) for line in f.read().splitlines()]
   
    # Part 1 Implementation  
    space_p1 = expand_space(space, 1)
    galaxies_p1 = find_galaxies(space_p1)
    res1 = 0

    for i in range(len(galaxies_p1)):
        for j in range(i+1, len(galaxies_p1)):
            res1 += find_distance(galaxies_p1[i],galaxies_p1[j]) 
   
    # Part 2 Implementation
    galaxies = find_galaxies(space)
    e_coord = find_empty_coord(space)
    res2 = 0

    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            res2 += find_distance_p2(galaxies[i],galaxies[j],e_coord,times=1_000_000) 

    # Printing Results
    print(f"Sum of all shortest distances between all galaxy pairs (Part 1): {res1}")    
    print(f"Sum of all shortest distances between all galaxy pairs (Part 2): {res2}")     
    
# Entry Point
if __name__ == '__main__':
    main()
