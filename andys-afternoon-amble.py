# import math
import random

class Hex:    
    # going counter-clockwise starting from the rightmost cell from center
    direction_vectors = [(1,0), (1,-1), (0,-1), (-1,0), (-1,1), (0,1)]
    
    def __init__(self, q,r):
        self.q = q
        self.r = r
        
    def __eq__(self, b):
        if not isinstance(b, Hex):
            return False
        return self.q == b.q and self.r == b.r
    
    def __hash__(self):
        return hash((self.q, self.r))
    
    def __str__(self):
        return f"({self.q}, {self.r})"
    
    # returns tuple, direction should always be a tuple
    def direction(direction):
        return Hex(direction[0], direction[1])

    # returns a Hex
    def add(hex, vec):
        return Hex(hex.q + vec.q, hex.r + vec.r)
    
    # returns a Hex
    def subtract(a,b):
        return Hex(a.q - b.q, a.r - b.r)
    
    def neighbour(hex, direction):
        return Hex.add(hex, Hex.direction(direction))
    
    # returns array of Hex listing all neighbours for given hex    
    def allNeighbours(self):
        neighbours = []
        for direction in Hex.direction_vectors:
            neighbours.append(Hex.neighbour(self, direction))
            
        return neighbours
    
    # returns array of Hex listing all white neighbours for given hex    
    def allWhiteNeighbours(self):
        neighbours = []
        for direction in Hex.direction_vectors:
            neighbour = Hex.neighbour(self, direction)
            if not neighbour.isBlackCell():
                neighbours.append(neighbour)
            
        return neighbours
    
    # returns array of Hex listing all black neighbours for given hex    
    def allBlackNeighbours(self):
        neighbours = []
        for direction in Hex.direction_vectors:
            neighbour = Hex.neighbour(self, direction)
            if neighbour.isBlackCell():
                neighbours.append(neighbour)
            
        return neighbours
    
    def distance(a,b):
        vec = Hex.subtract(a,b)
        return (abs(vec.q) + abs(vec.q + vec.r)+ abs(vec.r)) / 2
    
    def isBlackCell(self):
        return (self.q - self.r) % 3 == 0
    
    # given a Hex center and a range N, returns a list of Hexs
    def hexRange(center, N):
        results = []
        for q in range(-N, N+1):
            for r in range(max(-N, -q-N), min(N, -q+N)+1):
                results.append(Hex.add(center, Hex(q,r)))
                
        return results
    
# below are all white cells since 0,0 is a black cell. 
# lets just say home is (1,0)
# direction_vectors = [Hex(1,0), Hex(1,-1), Hex(0,-1), Hex(-1,0), Hex(-1,1), Hex(0,1)]

# radius of walkable space
R = 100
# number of trials
T = 1000000

res = Hex.hexRange(Hex(0,0), R)
# labels 0=home, 1,2,3

home = Hex(1,0)
cell1 = Hex(2,0)
cell2 = Hex(1,-1)
cell3 = Hex(0,1)
labels = {home: 0, cell1: 1, cell2: 2, cell3: 3}

queue = [home,cell1,cell2,cell3]

while len(queue) > 0:
    # hex to focus on for this loop
    currHex = queue.pop(0)
    
    for b in currHex.allBlackNeighbours():
        # gets the cell opposite from currCell 
        nextCellToLabel = Hex(2*b.q - currHex.q, 2*b.r - currHex.r)
        # error checking just in case
        if nextCellToLabel not in labels and Hex.distance(home, nextCellToLabel) <= R:
            labels[nextCellToLabel] = labels[currHex]
            queue.append(nextCellToLabel)

# each trial
# discoveries = 0
# for _ in range(T):
#     currHex = home
#     while True:
#         currHex = random.choice(currHex.allWhiteNeighbours())
#         # going back to the actual home does not count as a discovery
#         if currHex == home:
#             break
#         elif labels[currHex] == 0:
#             discoveries += 1
#             break
    
# p = discoveries/T
# # printing near 0.55
# print(f"p={p}")

# finding the probability of reaching home from every cell
numTotalCells = len(Hex.hexRange(home, R))
f = dict.fromkeys(list(labels), 0)
f[home] = 1
# p = probability of discovery
p = 0
for i in range(numTotalCells):
    prevP = p
    for cell in list(labels):
        if not cell == home and not labels[cell] == 0:
            neighbour = cell.allWhiteNeighbours()
            f[cell] = (f.get(neighbour[0],0.0) + f.get(neighbour[1],0.0) + f.get(neighbour[2],0.0)) / 3
    
    neighbour = home.allWhiteNeighbours()
    p = 1 - ((f.get(neighbour[0],0.0) + f.get(neighbour[1],0.0) + f.get(neighbour[2],0.0)) / 3)
    if (i % 10 == 0):
        print(f"currently at {i}")
    if (abs(p - prevP) < 1e-12):
        break

print(f"p = {p}")

# for testing purposes 
# randomly sample a hex and check its label and its neighbours label
# for _ in range(10):
#     randomHex = random.choice(list(labels))
#     print(f"randomHex {randomHex} label: {labels[randomHex]}")
#     for hex in randomHex.allWhiteNeighbours():
#         print(f"hex {hex} label: {labels[hex]}")