import sys
import re

# Input Vector
f = open(sys.argv[1], 'r')
in_colors = {'red': int(sys.argv[2]), 'green': int(sys.argv[3]), 'blue': int(sys.argv[4])}

ids = []
powers = []

# For each line in file (1 line = 1 game)
for id, line in enumerate(f):

    # Skipping empty lines
    if not line.strip():
        continue
    
    # Initializing for the game
    valid_game = True
    max_color  = {'red' : 0, 'green' : 0, 'blue' : 0}    

    # Getting sets list
    game = re.match(r'^Game\s+\d+\s*:\s+(.+)', line).group(1)
    sets = game.split(';')

    # For each set of a game, find the number of each color
    for s in sets:
        matches = re.findall(r'(\d+)\s+(\w+)', s)
        # and save the max number drawn for each color
        for m in matches:
            count, color = m
            max_color[color] = max(max_color[color], int(count))

    # If the max number drawn is superior to the value specified as input, the game is not valid
    for color in in_colors.keys():
        if max_color[color] > in_colors[color]:
            valid_game = False

    # Log ids for valid games
    if valid_game:
        ids.append(id+1)

    # Get power of the minimum set usable with the set drawn in this game (Part 2)
    power = max_color['red'] * max_color['green'] * max_color['blue']
    powers.append(power)

# Printing Results
print(f'Sum of all the valid game Ids (Part 1): {sum(ids)}')
print(f'Sum of all power of minimum sets (Part 2): {sum(powers)}')

