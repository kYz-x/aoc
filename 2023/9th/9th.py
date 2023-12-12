import sys
import math
import numpy as np 

f = open(sys.argv[1], 'r')

series = [list(map(int, line.split())) for line in f.read().splitlines()]
np_series = [np.ones((len(serie),len(serie))) for serie in series]

for i in range(len(series)):
    np_series[i][0,:] = series[i]

# Compute case value with the corresponding binomial coefficient
def compute_case(array, i, j):
    val = 0
    for l in range(j, i+j+1):
        val += ((-1) ** (i+(l-j))) * math.comb(i, l-j) * array[0,l] 
    return val

# Extrapolate case value 
def extrapolate_case(array, i, j):
    return array[i,j-1] + array[i+1,j-1]

res1, res2 = [], []

for serie in np_series:
    val = 0
    j = 0
    
    # There can only be n-1 substraction steps
    for i in range(1, len(serie[0])):
        j = 0
        serie[i,j] = compute_case(serie, i, j)
        
        while serie[i,j] == 0 and j < (len(serie[0])-i-1):
            j += 1
            serie[i,j] = compute_case(serie, i, j)
        
        # If the whole line equal to 0
        if serie[i,j] == 0:
            j += 1
            serie[i,j] = 0  # Set the next index to 0 and begin extrapolation
            max_i = i       # saving last i for the second way back for part 2
            
            ### Part 1 Implementation ###
            # We go back to i == 0 for extrapolation of the next value at the end of the history
            for i in range(max_i-1, 0, -1):
                # computing the case that was skip for faster descent
                serie[i, j] = compute_case(serie, i, j) 
                j += 1
                # extrapolating value based on elements (i,j-1) and (i+1,j-1)
                serie[i,j]    = extrapolate_case(serie, i, j)
                
            # appending last extrapolation at the end of the history
            res1 += [int(extrapolate_case(serie, i-1, j+1))]
            
            ### Part 2 Implementation ###
            # Extrapolation of of the previous value at the beginning of the history
            leftmost_val = [0] * (max_i+1)
            leftmost_val[max_i] = 0
            for i in range(max_i-1, -1, -1):
                leftmost_val[i] = serie[i, 0] - leftmost_val[i+1]
            
            # appending extrapolated previous history value result
            res2 += [int(leftmost_val[0])]
            
            break

# Printing Results 
print(f"Sum of all next extrapolated values (Part 1): {sum(res1)}")
print(f"Sum of all previous extrapolated values (Part 2): {sum(res2)}")
