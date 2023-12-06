import sys

def is_symbol(string):
    return ((not string.isdigit()) and (not (string == '.')))

# Get Integer Value of substring at position pos
def get_value(string, pos):
    val = []

    if string[pos].isdigit():
        val.append(string[pos])
    else:
        return -1
    
    # Right Parsing
    for i in range(pos+1, len(string)):
        if string[i].isdigit():
            val.append(string[i])
        else:
            break

    # Left Parsing
    for i in range(pos-1, -1, -1):
        if string[i].isdigit():
            val.insert(0, string[i])
        else:
            break

    return int(''.join(val))

f = open(sys.argv[1], 'r')
matrix = []

# Create a matrix of char with no carriage return
matrix  = [line.rstrip() for line in f]
parts = []

# Parse the matrix for symbol
for i in range(len(matrix)):
    for j in range(len(matrix[i])):

        if is_symbol(matrix[i][j]):
            # print(f'{matrix[i][j]} {is_symbol(matrix[i][j])}')
            part_val = []

            if j+1 < len(matrix[i]):
                part_val.append(get_value(matrix[i],j+1))
            if j-1 >= 0:
                part_val.append(get_value(matrix[i],j-1))
            if i+1 < len(matrix):
                part_val.append(get_value(matrix[i+1],j))
            if i-1 >= 0:
                part_val.append(get_value(matrix[i-1],j))

            parts += [val for val in part_val if val != -1]

print(parts)

# Printing Results
print(f'Sum of all part values: {sum(parts)}')

