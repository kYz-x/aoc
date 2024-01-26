import sys
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
        terrain = list(map(reversed, terrain))
    
    # Main Algorithm
    for lane in terrain:
        empty_space = []
        for i in range(len(lane)):
            if lane[i] == '.':
                empty_space.append(i)
            elif lane[i] == '#':
                empty_space.clear()
            elif empty_space and lane[i] == 'O':
                lane[empty_space.pop(0)] = 'O'
                lane[i] = '.'
                empty_space.append(i)
                
    # Recreating the initial list for south and east direction 
    if dir in [Dir.south, Dir.east]:
        terrain = list(map(reversed, terrain))    
    
    # Recreating the initial matrix for south and north direction
    if dir in [Dir.north, Dir.south]:
        terrain = list(map(list, zip(*terrain))) 
        
    return terrain

def compute_score(terrain):
    score = 0
    
    for i, line in enumerate(reversed(terrain)):
        score += sum([1 for c in line if c == 'O']) * (i+1)

    return score

def display(terrain):
    for line in terrain:
        print(''.join(line))
    print('')
    
def main():    
    # Parsing File
    f = open(sys.argv[1], 'r')
    terrain = [line for line in f.read().splitlines()]
    display(terrain)
    terrain = tilt(terrain, Dir.north)
    res1    = compute_score(terrain)
    display(terrain)
    
    # Printing Results
    print(f'Score after tilting north (Part 1): {res1}')
    
    
if __name__ == '__main__':
    main()