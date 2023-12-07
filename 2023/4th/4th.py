import sys

f = open(sys.argv[1], 'r')

lines = [line.rstrip() for line in f]
points = []
games = []

# Parse file for games 
for line in lines:
    game     = [e for e in line.split('|') if e != '']
    wincond  = list(map(int,[e for e in game[0].split(' ') if e != ''][2:]))
    card     = list(map(int,[e for e in game[1].split(' ') if e != '']))
    games.append((wincond, card))

# Part 1 Implementation
for game in games:
    wincond, card  = game
    point = 0

    point = sum(1 for c in card if c in wincond)
    
    points.append(point if not point else 2**(point-1))


# Part 2 Implementation
game_done = []

# For each card (ascending order)
for i in range(len(games)):
    wincond, card = games[i]
    n_matches = 0
    n_copies  = 1  # Taking into account the first card
    
    
    # There is one copie of each previous card copies where the match number reach this card id.
    for j in range(i-1, -1, -1):
        if j < 0:
            continue
        elif game_done[j][1] >= i-j:
            n_copies += game_done[j][0]   # there will be a copie for each copie of the previous card

    # Counting the number of matches used by the next cards in the iteration
    for c in card:                      
        if c in wincond:
            n_matches += 1

    game_done.append((n_copies, n_matches)) 

done = sum(g[0] for g in game_done)


# Printing Results
print(f'Sum of all game scores (Part 1): {sum(points)}')
print(f'Total scratchcards done (Part 2): {done}')
