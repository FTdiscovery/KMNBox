# players 1 (-1/A) and 2 (1/B)
# state is array of length m*n, values -1,0,1
# runGame() allows you to play and check all possible winning moves of a given
# player on a given state - the more moves already made in the state, or the
# more previous queries already evaluated, the faster the function.

# roughly 3 minutes initial runtime before commands can be run in IDLE
import time
import pickle
import numpy as np

"""
VARIABLES NEEDED:
m - width of board
n - height of board
CUTOFF - CUTOFF depth for search
mem - dictionary
trans - denotes where stones are
winSign - denotes where stone placements are winning for given player
"""
m = 11
n = 3
CUTOFF = 2
mem = {}
trans = ['.', 'B', 'A']
winSign = ['.', 'b', 'a', '.']  # ['.','b','a','.']

def encode(state):
    s = 0
    for i in range(m * n): s += (state[i] % 3) * 3 ** i
    return s

def move(state, i, toMove):
    newstate = []
    for j in range(m * n):
        if j == i:
            newstate.append(toMove)
        else:
            newstate.append(state[j])
    return newstate


def legal(state, p, z=False):
    possible = set()
    failed = set()
    if min(state) == max(state) and z:
        for i in range(int((n + 1) / 2)):
            for j in range(int((m + 1) / 2)):
                possible.add(i * m + j)
        return possible
    for i in range(m * n): possible.add(i)
    for i in range(m * n):
        if state[i] == p:
            if i - m >= 0: failed.add(i - m)
            if i % m != 0: failed.add(i - 1)
            if i % m != m - 1: failed.add(i + 1)
            if i + m < m * n: failed.add(i + m)
        if state[i] != 0: failed.add(i)
    return possible.difference(failed)

def printBoard(state, toMove):
    print("----")
    marginboard = []
    for i in range(n):
        marginboard.append([0] * m)
    for i in range(m * n):
        marginboard[i // m][i % m] = trans[state[i]]
    a = legal(state, toMove)
    for i in range(m * n):
        if i in a:
            newstate = move(state, i, toMove)
            b = check(newstate)
            if b:
                marginboard[i // m][i % m] = winSign[b + toMove]
            else:
                marginboard[i // m][i % m] = winSign[search(newstate, 0 - toMove, 3) + toMove]
        elif marginboard[i // m][i % m] == '.':
            marginboard[i // m][i % m] = 'x'
    print(trans[toMove] + ' to move\n')
    for i in range(n):
        for j in range(m):
            print(marginboard[i][j], end=' ')
        print('')
    print("----")

def check(state):
    try:
        a = mem[encode(state)]
    except KeyError:
        pass
    else:
        return a
    try:
        a = mem[encodeRR(state)]
    except KeyError:
        pass
    else:
        return a
    try:
        a = mem[encodeF(state)]
    except KeyError:
        pass
    else:
        return a
    try:
        a = mem[encodeFRR(state)]
    except KeyError:
        pass
    else:
        return a
    if m == n:
        try:
            a = mem[encodeR(state)]
        except KeyError:
            pass
        else:
            return a
        try:
            a = mem[encodeRRR(state)]
        except KeyError:
            pass
        else:
            return a
        try:
            a = mem[encodeFR(state)]
        except KeyError:
            pass
        else:
            return a
        try:
            a = mem[encodeRF(state)]
        except KeyError:
            pass
        else:
            return a

def encodeR(state):
    s = 0
    for i in range(m * n): s += (state[m * (i % m) + m - 1 - (i // m)] % 3) * 3 ** i
    return s


def encodeRR(state):
    s = 0
    for i in range(m * n): s += (state[m * (n - 1 - i // m) + m - 1 - (i % m)] % 3) * 3 ** i
    return s


def encodeRRR(state):
    s = 0
    for i in range(m * n): s += (state[m * (m - 1 - i % m) + (i // m)] % 3) * 3 ** i
    return s


def encodeF(state):
    s = 0
    for i in range(m * n): s += (state[m * (i // m) + m - 1 - (i % m)] % 3) * 3 ** i
    return s


def encodeFR(state):
    s = 0
    for i in range(m * n): s += (state[m * (m - 1 - i % m) + m - 1 - (i // m)] % 3) * 3 ** i
    return s


def encodeFRR(state):
    s = 0
    for i in range(m * n): s += (state[m * (n - 1 - i // m) + (i % m)] % 3) * 3 ** i
    return s


def encodeRF(state):
    s = 0
    for i in range(m * n): s += (state[m * (m - 1 - i % m) + m - 1 - (i // m)] % 3) * 3 ** i
    return s


def search(state, toMove, depth):
    solve = None
    solved = False
    try:
        solve = mem[encode(state)]
    except KeyError:
        pass
    else:
        solved = True
    if solved: return solve
    a = legal(state, toMove, z=True)
    if len(a) < 1:
        mem[encode(state)] = sum(state)
        return sum(state)
    else:
        best = -2
        for i in a:
            newstate = move(state, i, toMove)
            b = search(newstate, 0 - toMove, depth + 1)
            best = max(best, b * toMove)
            if 2 * best + toMove > 0: break
        mem[encode(state)] = best * toMove
        if depth <= CUTOFF:
            for i in range(n):
                for j in range(m):
                    print(trans[state[i * m + j]], end=' ')
                print('')
            print('of depth ' + str(depth) + ' has winner p' + str(best * toMove + 2) + '\n')
        if len(mem) % 1000000 == 0:
            print("states in memory:", len(mem))
        return best * toMove

start = time.time()
try:
    mem = pickle.load(open("AdamLog/"+str(m)+"x"+str(n)+"log.pkl", "rb"))
except:
    a = search([0] * (m * n), -1, 0)
    f = open("AdamLog/"+str(m)+"x"+str(n)+"log.pkl", "wb")
    pickle.dump(mem, f)
    f.close()
end = time.time()
print("Time elasped:", end - start, "seconds.")


def runGame():
    print("---")
    state = [0] * m * n
    toMove = -1
    a = legal(state, toMove)
    turns = 0
    while a:
        want = input('Player ' + trans[toMove] + ' move: ')
        try:
            want = int(want)
        except ValueError:
            pass
        while want not in a:
            print("illegal move")
            want = input('Player ' + trans[toMove] + ' move: ')
            try:
                want = int(want)
            except ValueError:
                pass
        state = move(state, want, toMove)
        toMove = 0 - toMove
        turns += 1
        if turns > 1: printBoard(state, toMove)
        a = legal(state, toMove)
    print('Player ' + trans[toMove] + ' loses')


runGame()
