
from time import time
from BFS_search import breadth_first_search
from Astar_search import Astar_search
from RBFS_search import recursive_best_first_search
from puzzle import Puzzle

def generate_matrix_spiral(n):
    matrix = [[0 for x in range(n)] for y in range(n)]
    num = 1
    for layer in range(n//2):
        first, last = layer, n-layer-1
        for i in range(first, last):
            matrix[layer][i] = num
            num += 1
        for i in range(layer, last):
            matrix[i][last] = num
            num += 1
        for i in range(last, first, -1):
            matrix[last][i] = num
            num += 1
        for i in range(last, first, -1):
            matrix[i][first] = num
            num += 1
    if n % 2 == 1:
        matrix[n//2][n//2] = num
    return matrix

def getInvCount(state):
    inv_count = 0
    empty_value = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if state[j] != empty_value and state[i] != empty_value and state[i] > state[j]:
                inv_count += 1
    print(inv_count)
    return inv_count



def isSolvable(state):
    inv_count = getInvCount(state)
    return (inv_count % 2 == 0)

state=[[1, 2, 3,
        4, 5, 6,
        7, 0, 8],

       [1, 2, 3,
        4, 5, 6,
        7, 0, 8],

       [1, 2, 3,
        4, 6, 5,
        7, 0, 8]]

for i in range(len(state)):
    if(isSolvable(state[i])):
        Puzzle.num_of_instances=0
        t0=time()
        bfs=breadth_first_search(3,state[i])
        t1=time()-t0
        print('BFS:', bfs)
        print('space:',Puzzle.num_of_instances)
        print('time:',t1)
        print()

        Puzzle.num_of_instances = 0
        t0 = time()
        astar = Astar_search(3,state[i])
        t1 = time() - t0
        print('A*:',astar)
        print('space:', Puzzle.num_of_instances)
        print('time:', t1)
        print()

        Puzzle.num_of_instances = 0
        t0 = time()
        RBFS = recursive_best_first_search(3,state[i])
        t1 = time() - t0
        print('RBFS:',RBFS)
        print('space:', Puzzle.num_of_instances)
        print('time:', t1)
        print()
    else:
        print("Can't solve")
        print('------------------------------------------')