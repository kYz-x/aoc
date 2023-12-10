import sys

f = open(sys.argv[1], 'r')

# Unitary card value
c_val = {
        '2'  :  1,
        '3'  :  2,
        '4'  :  3,
        '5'  :  4,
        '6'  :  5,
        '7'  :  6,
        '8'  :  7,
        '9'  :  8,
        'T'  :  9,
        'J'  : 10,
        'Q'  : 11,
        'K'  : 12,
        'A'  : 13
        }

# Hnad types enumeration
class hType: 
    _HC = 1
    _1P = 2
    _2P = 3
    _3K = 4
    _FH = 5
    _4K = 6
    _5K = 7


class Hand:

    # A Hand is a string of card values associated with a bid value
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid  = bid

    def getType(self, joker=False):
        count = {} 
        
        # Count the number for each card in the hand
        for i in range(len(self.hand)):
            val = self.hand[i]
            if val in count.keys():
                count[val] += 1
            else:
                count[val] = 1

        # If there is a joker in the hand
        if joker and 'J' in count.keys():
            num_joker  = count['J']  
            count['J'] = 0 
            max_key = max(count,key=count.get)
            count[max_key] += num_joker 
       
        # Get highest numbers at the beginning of the list
        lcount = sorted(count.values(), reverse=True)
        
        # Return Type (Highest Card, 1 Pair, 2 Pairs, ...)
        if lcount[0] == 5:
            return hType._5K
        elif lcount[0] == 4:
            return hType._4K
        elif lcount[0] == 3 and lcount[1] == 2:
            return hType._FH
        elif lcount[0] == 3:
            return hType._3K
        elif lcount[0] == 2 and lcount[1] == 2:
            return hType._2P
        elif lcount[0] == 2:
            return hType._1P
        else:
            return hType._HC

    # Look if the hand is greater by type (then highest card if equal) against another hand
    def isGreater(self, hand, joker=False):

        # return True (greater) or False (less)
        if self.getType(joker) > hand.getType(joker):
            return True
        elif self.getType(joker) < hand.getType(joker):
            return False
        
        #print(f'{self.hand} same as {hand}')
        
        # If both are are the same type, look at the highest card value
        for i in range(len(self.hand)):
            
            if joker and hand.hand[i] == 'J' and self.hand[i] != 'J':
                return True
            elif joker and hand.hand[i] != 'J' and self.hand[i] == 'J':
                return False
            elif c_val[self.hand[i]] > c_val[hand.hand[i]]:
                return True
            elif c_val[self.hand[i]] < c_val[hand.hand[i]]:
                return False

            #print(f'{self.hand[i]} is equal to {hand.hand[i]}')

        return True  
        
    def __str__(self):
        return str((self.hand, self.bid)) 

# Quicksort Algorithm
def quicksort_hands(hands, joker=False):
    if len(hands) == 0:
        return hands
    
    pivot = hands[0]
    arr_lower   = []
    arr_greater = []

    for hand in hands[1:]:
        if pivot.isGreater(hand, joker):
            arr_lower += [hand]
        else:
            arr_greater += [hand]

    return quicksort_hands(arr_lower,joker) + [pivot] + quicksort_hands(arr_greater,joker)

# Parsing file and create Hand data objects 
hands = [tuple(line.split()) for line in f.read().splitlines()]
hands = list(map(lambda x: Hand(x[0], int(x[1])), hands))

# Sorting Part 1 and Part 2 hands
hands_sorted_p1 = quicksort_hands(hands, joker=False)
hands_sorted_p2 = quicksort_hands(hands, joker=True)

# Computing Final Results
res1, res2 = 0, 0
for rank, hand in enumerate(hands_sorted_p1):
    res1 += (rank+1) * hand.bid

for rank, hand in enumerate(hands_sorted_p2):
    res2 += (rank+1) * hand.bid

# Printing Results
print(f'Sum of all bid x rank (Part 1): {res1}')
print(f'Sum of all bid x rank with joker rule (Part 2): {res2}')


