import sys

# Find line of reflexion with exactly n_smudges element off
def find_line(pat, n_smudges=0):
    lines = []
    
    # Line by Line Parsing
    for i in range(len(pat)-1):
        smudges = num_smudge(pat[i], pat[i+1])
        if smudges <= n_smudges:
            lines += [(i+1, smudges)]

    for line, smudges in lines:
        for i in range(1,len(pat)-1):
            if line-1-i < 0 or line+i >= len(pat):   # If all lines up to the end are reflected
                if smudges == n_smudges:             # with exactly one smudge
                    return line            
                else:                                # else, reflexion line is not valid
                    continue    
            
            smudges += num_smudge(pat[line-1-i], pat[line+i])
           
            if smudges > n_smudges:                # Not a real line of reflexion if not all lines are reflected
                continue
            
    return 0

def num_smudge(line_a, line_b):
    smudge = 0
    
    for i in range(len(line_a)):
        if line_a[i] != line_b[i]:
            smudge += 1
            
    return smudge
    
# Main Function
def main():
    
    # Parsing File
    f = open(sys.argv[1], 'r')
    patterns = []
    pat = []
    
    for line in f.read().splitlines():
        if not line:
            patterns += [pat]
            pat = []
        else:
            pat += [line]
    patterns += [pat] 
    
    # Part 1 Implementation  
    res1 = 0
    res2 = 0
    
    # For each pattern in file
    for id, pat in enumerate(patterns):
        # Creating the transpose matrix
        pat_t = list(map(list, zip(*pat)))
        
        # Find perfect horizontal and vertical lines of reflextion
        num_up_lin, num_left_col = find_line(pat), find_line(pat_t)   
        # num_up_lin, num_left_col = find_line(pat), find_line(pat_t)   
        
        # Computing result of Part 1
        res1 += num_up_lin * 100 + num_left_col 
        
        # Find horizontal and vertical lines of reflextion (with exactly 1 smudge)
        num_up_lin = find_line(pat,1)
        if num_up_lin:                   # if reflexion found in horizontal dimension, no reflexion to be found in vertical dimension
            num_left_col =  0
        else:                            # else, it the reflexion line must be found in vertical dimension
            num_left_col = find_line(pat_t, 1)   
        
        # Computing result of Part 2
        res2 += num_up_lin * 100 + num_left_col 
    
    # Printing Results
    print(f"Result for Part 1: {res1}")  
    print(f"Result for Part 2: {res2}")   
    
# Entry Point
if __name__ == '__main__':
    main()
