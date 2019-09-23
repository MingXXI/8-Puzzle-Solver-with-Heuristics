# a1.py

import time
import random
from search import *
from test_search import *


### Question 1 ##########################################################################

def make_rand_8puzzle():
    initial_state = [x for x in range(9)]
    random.shuffle(initial_state)
    obj = EightPuzzle(initial_state)
    while EightPuzzle.check_solvability(EightPuzzle,initial_state) != 0:
        random.shuffle(initial_state)
            
    return initial_state
    
def display(state):
    for i in range(3):
        for j in range (3):
            if state[i*3+j] == 0:
                print("*", end = '')
            else :
                print(state[i*3+j], end = '')
            if j != 2:
                print(" ", end = '')
        print('')

### Question 2 ################################################################
    
def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    rm_count = 0
    while frontier:
        node = frontier.pop()
        rm_count += 1
        if problem.goal_test(node.state):
            return node, rm_count
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def mht(node):  ## this function is from: https://codereview.stackexchange.com/questions/110429/8-puzzle-using-a-and-manhattan-distance
    mhtd = 0
    state = list(node.state)
    for counter, value in enumerate(state):
        if value:
            index = value - 1
            mhtd = mhtd + abs(index//3 - counter//3) + abs(index%3 - counter%3)
    return mhtd

def mot(node):
        n = EightPuzzle(node.state)
        return max(mht(node),n.h(node))



for i in range(10):
        x = make_rand_8puzzle();

        print(x)
        
        start_time = time.time()
        mth, node_removed = astar_search(x)
        elapsed_time = time.time() - start_time
        print('Puzzle No.', i+1, ' solved using misplaced tile heuristic in ', elapsed_time, 'seconds with ',len(mth.solution()),' moves and ',node_removed,' nodes removed from frontier\n')
        
        start_time = time.time()
        mdh, node_removed = astar_search(x, h = mht)
        elapsed_time = time.time() - start_time
        print('Puzzle No.', i+1, ' solved using Manhattan distance heuristic in ', elapsed_time, 'seconds with ',len(mdh.solution()),' moves and ',node_removed,' nodes removed from frontier\n')

        start_time = time.time()
        mh, node_removed = astar_search(x, h = mot)
        elapsed_time = time.time() - start_time
        print('Puzzle No.', i+1, ' solved using max of misplaced tile heuristic and Manhattan distance heuristic in ', elapsed_time, 'seconds with ',len(mh.solution()),' moves and ',node_removed,' nodes removed from frontier\n\n\n')


        


