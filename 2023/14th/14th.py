import sys
import copy
from enum import Enum

class Dir(Enum):
    north = 0
    south = 1
    west  = 2
    east  = 3


def tilt(terrain, dir):

    # Creating transpose matrix for south and north direction
    if dir in [Dir.north, Dir.south]:
        terrain = list(map(list, zip(*terrain)))
    
    # Reverse list for south and east direction 
    if dir in [Dir.south, Dir.east]:
        terrain = list(map(list,map(reversed, terrain)))
    
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

                
    # Recreating the initial list for south and east direction 
    if dir in [Dir.south, Dir.east]:
        terrain = list(map(list,map(reversed, terrain)))
    
    # Recreating the initial matrix for south and north direction
    if dir in [Dir.north, Dir.south]:
        terrain = list(map(list, zip(*terrain))) 
    
    return terrain

def compute_score(terrain):
    score = 0
    
    for i, line in enumerate(reversed(terrain)):
        score += sum([1 for c in line if c == 'O']) * (i+1)

    return score

def compute_cycle(terrain, cycles):
    history = []
    final_score  = 0
    
    history.append(copy.deepcopy(terrain))
    
    for i in range(cycles):
        terrain = tilt(terrain, Dir.north)
        terrain = tilt(terrain, Dir.west)
        terrain = tilt(terrain, Dir.south)
        terrain = tilt(terrain, Dir.east)

        # If the first pattern in a period is detected
        if terrain in history:
            break

        history.append(copy.deepcopy(terrain))
    
    # Find period length and first index in history
    first_idx = history.index(terrain)
    period_len = len(history) - first_idx
    
    # Find the index within the period for the final iteration
    final_idx = ((cycles - first_idx) % period_len) + first_idx    
    final_terrain = history[final_idx]
    final_score = compute_score(final_terrain)
    
    return final_score

# Display terrain in ASCII format
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
    res2 = compute_cycle(terrain_p2, 1_000_000_000)
    
    # Printing Results
    print(f'Score after tilting north (Part 1): {res1}')
    print(f'Score after 1e9 cycles (Part 2): {res2}')
    
    
if __name__ == '__main__':
    main()