import sys

# Find line of reflexion
def find_line(pat):
    lines = []
    
    # Line by Line Parsing
    for i in range(len(pat)-1):
        if pat[i] == pat[i+1]:
            lines += [i+1]

    for line in lines:
        for i in range(1,len(pat)-1):
            if line-1-i < 0 or line+i >= len(pat):   # If all lines up to the end are reflected
                return line 
            if pat[line-1-i] != pat[line+i]:        # Not a real line of reflexion if not all lines are reflected
                break
            
    return 0

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
    
    for pat in patterns:
        
        # Find horizontal line of reflextion
        num_up_lin = find_line(pat)  
        
        # Creating the transpose matrix
        pat_t = list(map(list, zip(*pat)))
        
        # Find vertical line of reflextion
        num_left_col = find_line(pat_t)  

        res1 += num_up_lin * 100 + num_left_col 
    
    # Printing Results
    print(f"Result from part 1 (Part 1): {res1}")    
    
# Entry Point
if __name__ == '__main__':
    main()
