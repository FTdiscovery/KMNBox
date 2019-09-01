import pickle
import time

#board: 1's are player to move's squares, and -1's are other's
#(however, it's changed to p1, p2 for display)
dim = [5,5]

states = dict() #dict of all previously seen states
newstate = 0 #times program saves a new state into states
oldstate = 0 #times program recalls a state it's seen before
pthresh = 2 #print if board's in the first pthresh moves
proginter = 10000 #print new/oldstate in this increment

def solve(board): # returns whether player to move wins
    if lookup(board) != None:
        global oldstate
        oldstate += 1
        if oldstate%proginter == 0:
            print("oldstate: " + str(oldstate))
        return lookup(board)
    winning = False
    for i in range(dim[0]):
        for j in range(dim[1]):
            #print(board, [i, j], valid(board, [i, j]))
            if valid(board, [i, j]):
                newboard = clone(board)
                newboard[i][j] = 1
                newboard = flip(newboard)
                if solve(newboard) == False:
                    winning = True
                    break
        if winning == True:
            break
    if abssum(board) <= pthresh:
        print(pfriendly(board), "player",
              str(2-(int(winning)+abssum(board))%2),
              "wins", "move:", abssum(board))
    states.update({tonumber(board) : winning})
    global newstate
    newstate += 1
    if newstate%proginter == 0:
        print("newstate: " + str(newstate))
    return winning

def valid(board, move): #returns whether move (x,y) is valid
    if get(board, move) != 0:
        return False
    isvalid = True
    for i in range(4):
        adj = [move[0]+(1-i%2)*(-1)**(i//2), move[1]+(i%2)*(-1)**(i//2)]
        if inside(adj) and get(board, adj) == 1:
            isvalid = False
    return isvalid


def inside(square): #returns whether square (x,y) is within bounds
    return square[0] in range(dim[0]) and square[1] in range(dim[1])

def get(board, square): #literally gets value of board at square
    return board[square[0]][square[1]]

def tonumber(board): #integer rep of board (acts as key in states)]
    boardnum = 0
    for row in reversed(pfriendly(board)):
        for x in reversed(row):
##            boardnum = boardnum + str(x)
            boardnum *= 3
            boardnum += x
    return boardnum

def toarray(boardnum): #inverse operation of tonumber
##    if len(boardstr) != dim[0]*dim[1]:
##        return None
    nboard = [[] for i in range(dim[0])]
    for ind in range(dim[0]*dim[1]):
        nboard[ind//dim[1]].append(boardnum%3)
        boardnum//=3
    return pangery(nboard)

def abssum(board): #sum of absolute values (how many moves have elapsed)
    count = 0
    for row in board:
        for x in row:
            count += abs(x)
    return count


#transformations (not in-place methods):
def clone(board): #returns clone
    nboard = []
    for row in board:
        nboard.append([x for x in row])
    return nboard

def horiz(board): #reflection about y-axis
    nboard = []
    for row in board:
        nboard.append([x for x in reversed(row)])
    return nboard

def vert(board): #reflection about x-axis
    nboard = []
    for row in reversed(board):
        nboard.append([x for x in row])
    return nboard

def transp(board): #transpose, only to be used when square
    nboard = []
    nboardzip = zip(*board)
    for nrow in nboardzip:
        nboard.append([x for x in nrow])
    return nboard

def flip(board): #*-1 to each entry
    nboard = []
    for row in board:
        nboard.append([-1*x for x in row])
    return nboard

def pfriendly(board): #turns {player to move: 1, other: -1} into {player 1: 1, player 2: 2}
    if abssum(board)%2 == 0:
        xboard = clone(board)
    else:
        xboard = flip(board)
    nboard = []
    for row in xboard:
        nboard.append([(3*x*x-x)//2 for x in row])
    return nboard

def pangery(board): #inverse of pfriendly
    xboard = []
    for row in board:
        xboard.append([(5*x-3*x*x)//2 for x in row])
    if abssum(xboard)%2 == 0:
        nboard = clone(xboard)
    else:
        nboard = flip(xboard)
    return nboard

#for previously made logs
def loadlog():
    global states
    states = pickle.load(open(str(dim[0])+"x"+str(dim[1])+" log.pkl", "rb"))

def lookup(board):
    for i in range(8):
        symboard = clone(board)
        if i%2 == 1:
            symboard = horiz(symboard)
        if (i//2)%2 == 1:
            symboard = vert(symboard)
        if i//4 == 1:
            if dim[0] == dim[1]:
                symboard = transp(symboard)
            else:
                break
        #print(symboard)
        #print(tonumber(symboard))
        if states.get(tonumber(symboard)) != None:
            return states.get(tonumber(symboard))
    return None


#board: 1's are player to move's squares, and -1's are other's
start = time.time()
board = [[0]*dim[1] for i in range(dim[0])]
solve(board)
end=time.time()
print(end-start)
print(oldstate, newstate)
f = open(str(dim[0])+"x"+str(dim[1])+" log.pkl", "wb")
pickle.dump(states, f)
f.close()
print(len(states))



def lookupstr(boardstr):
    if len(boardstr) != dim[0]*dim[1]:
        return None
    board = [[] for i in range(dim[0])]
    for ind in range(dim[0]*dim[1]):
        board[ind//dim[1]].append(int(boardstr[ind]))
    #print(board)
    return lookup(pangery(board))


