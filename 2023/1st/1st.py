import sys

f = open(sys.argv[1], 'r')
cal_val = []
dig = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six' : 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def find_all_substring(string, substring):
    idx = []
    start = 0
    pos = 0

    while pos != -1:
        pos = string.find(substring,start)
        if pos != -1:
            start = pos + 1
            idx.append(pos)

    return idx

# For each line in file 
for line in f:
    # Initialization
    first_pos = float('inf')
    last_pos = -1

    # First Pass: recognize digit 
    for pos, char in enumerate(line):
        if char.isdigit():
            if pos < first_pos:
                first_dig, first_pos = char, pos
            if pos > last_pos:
                last_dig, last_pos = char, pos

    # Second Pass: recognize digit spelled with letters
    for d in dig.keys():
        pos_list = find_all_substring(line,d)
        for pos in pos_list:
            if pos < first_pos:
                first_dig, first_pos = str(dig[d]), pos
            if pos > last_pos:
                last_dig, last_pos = str(dig[d]), pos
    
    # If at least a digit as been parsed
    if first_pos < len(line):
        cal_val.append(int(first_dig + last_dig))
        print(f'{line} = {first_dig+last_dig}')

# Print Result
print(f'Sum of all calibration values: {sum(cal_val)} {len(cal_val)}')

