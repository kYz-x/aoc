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

def sim_board(board, start_beam):
    score_board = [['.' for _ in range(len(board[0]))] for _ in range(len(board))]
    beams = [start_beam]
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
        
    return compute_score(score_board)   

# File Preprocessing
f = open(sys.argv[1], 'r')
board = list(map(list,f.read().splitlines()))
board_p1 = board
board_p2 = copy.deepcopy(board)

# Part 1 Implementation
dx, dy = 1, 0
x , y  = -1, 0
res1 = sim_board(board_p1, Beam(x,y,dx,dy))

# Part 2 Implementation
score_list = []
for i in range(len(board)*4):
    print(i)
    if i / len(board) < 1:
        x, y, dx, dy = -1, i%len(board), 1, 0
    if i / len(board) < 2:
        x, y, dx, dy = len(board[0]), i%len(board), -1, 0
    if i / len(board) < 3:
        x, y, dx, dy = i%len(board), -1, 0, 1
    else:    
        x, y, dx, dy = i%len(board), len(board), 0, -1

    start_beam = Beam(x,y,dx,dy)
    new_board  = copy.deepcopy(board_p2)
    score = sim_board(new_board, start_beam)
    score_list.append(score)

res2 = max(score_list)

# Printing Results
print(f'Number of energized tiles (Part 1): {res1}')
print(f'Maximum number of energized tiles (Part 2): {res2}')