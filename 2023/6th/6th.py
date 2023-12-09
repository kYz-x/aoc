import sys

f = open(sys.argv[1], 'r')
lines    = [line for line in f.read().splitlines() if line != '']
time     = [int(num) for num in lines[0].split()[1:] if num != '']
record   = [int(num) for num in lines[1].split()[1:] if num != '']

res_race = []
res = 1

### Part 1 Implementation ###
for race in range(len(time)):
    beat = 0

    for t in range(time[race]+1):
        dist = t * (time[race] - t)
        if dist > record[race]:
            beat += 1

    res_race += [beat]
    res      *= beat

### Part 2 Implementation ###
time   = int(''.join(map(str,time)))
record = int(''.join(map(str,record)))

beat = 0

for t in range(time+1):
    dist = t * (time - t)
    if dist > record:
        beat += 1

print(f"Mult. of all possibility to beat the record (Part 1): {res}")
print(f"Number of possibility to beat the record (Part 2): {beat}")
