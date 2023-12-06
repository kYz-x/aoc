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

# Create a matrix of char with no carriage return
matrix  = [line.rstrip() for line in f]
parts = []
gear_ratios = []

# Parse the matrix for symbol
for i in range(len(matrix)):
    for j in range(len(matrix[i])):

        # If it is a symbol (not a digit or a point '.')
        if is_symbol(matrix[i][j]):
            part_val = []

            # Find in all numbers adjacent to the symbole
            for k in range(-1,2):
                last_value = -1
                for l in range(-1,2):
                    if i+k < len(matrix) and i+k >= 0 and j+l < len(matrix[j+l]) and j+l >= 0:
                        value = get_value(matrix[i+k],j+l)

                        # Log the number if it is one and it is not the same number as in the previous position
                        if value != -1 and last_value == -1:
                            part_val.append(get_value(matrix[i+k],j+l))

                        last_value = value

            # Finding Gear Ratios
            if matrix[i][j] == '*' and len(part_val) == 2:
                gear_ratios.append(part_val[0] * part_val[1])

            parts += part_val


# Printing Results
print(f'Sum of all part values (Part 1): {sum(parts)}')
print(f'Sum of all gear ratios (Part 2): {sum(gear_ratios)}')

