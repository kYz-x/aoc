import sys
import copy
from enum import Enum

class Dir(Enum):
    north = 0
    south = 1
    west  = 2
    east  = 3


def tilt(terrain, dir, track_pos=[0,0]):

    # print(f'{dir} {terrain}')
    pos = track_pos[:]

    # Creating transpose matrix for south and north direction
    if dir in [Dir.north, Dir.south]:
        pos = [pos[1],pos[0]]
        terrain = list(map(list, zip(*terrain)))
    
    # print(f'{dir} {terrain}')

    # Reverse list for south and east direction 
    if dir in [Dir.south, Dir.east]:
        pos = [len(terrain[0])-1-pos[0], pos[1]]
        terrain = list(map(list,map(reversed, terrain)))
    
    # print(f'{dir} {terrain}')

    # Main Algorithm
    for j, lane in enumerate(terrain):
        empty_space = []
        for i in range(len(lane)):
            if lane[i] == '.':
                empty_space.append(i)
            elif lane[i] == '#':
                empty_space.clear()
            elif empty_space and lane[i] == 'O':
                new_pos = empty_space.pop(0)
                lane[new_pos] = 'O'
                lane[i] = '.'
                empty_space.append(i)

                # Track pos of rock at position pos
                if [i,j] == pos:
                    pos = [new_pos,j]
                
    # Recreating the initial list for south and east direction 
    if dir in [Dir.south, Dir.east]:
        pos = [len(terrain[0])-1-pos[0], pos[1]]
        terrain = list(map(list,map(reversed, terrain)))
    
    # Recreating the initial matrix for south and north direction
    if dir in [Dir.north, Dir.south]:
        pos = [pos[1],pos[0]]
        terrain = list(map(list, zip(*terrain))) 
    
    track_pos[:] = pos[:]

    return terrain

def compute_score(terrain):
    score = 0
    
    for i, line in enumerate(reversed(terrain)):
        score += sum([1 for c in line if c == 'O']) * (i+1)

    return score

def do_cycle(terrain, init_pos):
    score_cycle = []
    pos_cycle = []
    state = Dir.north
    terrain_c = copy.deepcopy(terrain)
    pos = [init_pos[0], init_pos[1]]
    
    pos_cycle.append(pos)
    while True:
        score_cycle.append(len(terrain) - pos[1])  # add scores
        terrain_c = tilt(terrain_c, state, track_pos=pos)
        pos_cycle.append(pos)
        print(pos)

        if state == Dir.north:
            state = Dir.west
        elif state == Dir.west:
            state = Dir.south
        elif state == Dir.south:
            state = Dir.east
        else:
            state = Dir.north

        # if pos == init_pos:
        if len(score_cycle) > 200:
            break

    return score_cycle


def find_cycle(list):
    cycle
    


def compute_cycle(terrain, cycles):
    score_cycles = []
    final_score  = 0
    
    # for y, line in enumerate(terrain):
    #     for x, char in enumerate(line):
    #         if char == 'O':
    #             print((x,y))
    #             score_cycles.append(find_cycle(terrain, (x,y)))
    score_cycles.append(do_cycle(terrain, (0,0)))

    final_score = sum([score[cycles % len(score)] for score in score_cycles])

    return final_score

def display(terrain):
    for line in terrain:
        print(''.join(line))
    print('')
    
def main():    
    # Parsing File
    f = open(sys.argv[1], 'r')
    terrain = [line for line in f.read().splitlines()]
    terrain_p2 = copy.deepcopy(terrain)

    # Part 1 Implementation 
    terrain = tilt(terrain, Dir.north)
    res1    = compute_score(terrain)
    
    # Part 2 Implementation
    # res2 = compute_cycle(terrain_p2, 1_000_000_000)
    res2 = compute_cycle(terrain_p2, 1)
    # pos = [0,0]
    # print(pos)
    # display(terrain_p2)
    # terrain_p2 = tilt(terrain_p2, Dir.north, track_pos=pos)
    # print(f'after north: {pos}')
    # display(terrain_p2)
    # terrain_p2 = tilt(terrain_p2, Dir.west,  track_pos=pos)
    # print(f'after west: {pos}')
    # display(terrain_p2)
    # terrain_p2 = tilt(terrain_p2, Dir.south, track_pos=pos)
    # print(f'after south: {pos}')
    # display(terrain_p2)
    # terrain_p2 = tilt(terrain_p2, Dir.east,  track_pos=pos)
    # print(f'after east: {pos}')
    # display(terrain_p2)
    # terrain_p2 = tilt(terrain_p2, Dir.north, track_pos=pos)
    # terrain_p2 = tilt(terrain_p2, Dir.west,  track_pos=pos)
    # terrain_p2 = tilt(terrain_p2, Dir.south, track_pos=pos)
    # terrain_p2 = tilt(terrain_p2, Dir.east,  track_pos=pos)
    # display(terrain_p2)
    # terrain_p2 = tilt(terrain_p2, Dir.north, track_pos=pos)
    # terrain_p2 = tilt(terrain_p2, Dir.west,  track_pos=pos)
    # terrain_p2 = tilt(terrain_p2, Dir.south, track_pos=pos)
    # terrain_p2 = tilt(terrain_p2, Dir.east,  track_pos=pos)
    # display(terrain_p2)

    # Printing Results
    print(f'Score after tilting north (Part 1): {res1}')
    print(f'Score after 1e9 cycles (Part 2): {res2}')
    
    
if __name__ == '__main__':
    main()