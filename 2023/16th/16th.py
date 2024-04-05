import sys
import copy

class Beam:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
    
def compute_score(score_board):
    return sum([sum([1 for c in line if c == '#']) for line in score_board])

def display(board):
    for line in board:
        print(''.join(line))
    print('')

# File Preprocessing
f = open(sys.argv[1], 'r')
board = list(map(list,f.read().splitlines()))
board_p1 = board
board_p2 = copy.deepcopy(board)

# Part 1 Implementation
dx, dy = 1, 0
x , y  = -1, 0
score_board = [['.' for _ in range(len(board[0]))] for _ in range(len(board))]
beams = [Beam(x,y,dx,dy)]
beam_hist = []

while beams:
    beam = beams[0]
    
    if (beam.x,beam.y,beam.dx,beam.dy) in beam_hist:
        beams.pop(0)
        continue
    else:
        beam_hist.append((beam.x,beam.y,beam.dx,beam.dy))
    
    if (beam.y + beam.dy) >= len(board) or (beam.x + beam.dx) >= len(board[0]) or \
       (beam.y + beam.dy) < 0 or (beam.x + beam.dx) < 0:
        beams.pop(0)
        continue
    else:    
        next_case = board[beam.y + beam.dy][beam.x + beam.dx]

    beam.x = beam.x + beam.dx
    beam.y = beam.y + beam.dy
    score_board[beam.y][beam.x] = '#'
    
    if next_case == '.':
        pass
    elif next_case == '|':
        if beam.dx == 1 or beam.dx == -1:
            beam.dx = 0
            beam.dy = 1
            beams.append(Beam(beam.x,beam.y,beam.dx,-beam.dy))
    elif next_case == '-':
        if beam.dy == 1 or beam.dy == -1:
            beam.dx = 1
            beam.dy = 0
            beams.append(Beam(beam.x,beam.y,-beam.dx,beam.dy))
    elif next_case == '/':
        tmp = -beam.dx
        beam.dx = -beam.dy
        beam.dy = tmp
    elif next_case == '\\':
        tmp = beam.dx
        beam.dx = beam.dy
        beam.dy = tmp
    else:
        raise Exception(f'character {next_case} not recognized.')
    
    
res1 = compute_score(score_board)       

# Part 2 Implementation
# TODO

display(score_board)

# Printing Results
print(f'Number of energized tiles (Part 1): {res1}')