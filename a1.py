# a1.py
# Student Name: Bowen Wang
# Student ID  : 301267523



from search import *
import random
import time

class EightPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j]!= 0:
                    inversion += 1

        return inversion % 2 == 0
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum((s != 0 and s != g) for (s, g) in zip(node.state, self.goal))


class YPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        ######### Corner Cases for Y-Puzzle #########
        
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 2 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('LEFT')

        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('RIGHT')

        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 3:
            possible_actions.remove('UP')

        if index_blank_square == 5 or index_blank_square == 7 or index_blank_square == 8:
            possible_actions.remove('DOWN')

        return possible_actions
    
    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        neighbor = blank + delta[action]

        if blank == 0:
            neighbor -= 1
        elif blank == 8:
            neighbor += 1
        elif blank == 6 and action == 'DOWN':
            neighbor -= 1
        elif blank == 2 and action == 'UP':
            neighbor += 1

        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)
    
    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        blank = state.index(0)

        if blank == 0:
            if state[1] != 2 or state[2] != 1 or state[8] != 7:
                return False
        elif blank == 1:
            if state[0] != 1 or state[4] != 2 or state[8] != 7:
                return False

        elif blank == 8:
            if state[0] != 1 or state[1] != 2 or state[6] != 7:
                return False

        else:
            if state[0] != 1 or state[1] != 2 or state[8] != 7:
                return False

        inversion = 0
        for i in range(2,8):
            for j in range(i+1, 8):
                if (state[i] > state[j]) and state[i] != 0 and state[j]!= 0:
                    inversion += 1


        return inversion % 2 == 0
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum((s != 0 and s != g) for (s, g) in zip(node.state, self.goal))

def make_rand_8puzzle():
    initial_state = [x for x in range(9)]
    random.shuffle(initial_state)
    rand_state = EightPuzzle(initial_state)
    while rand_state.check_solvability(initial_state) != True:
        random.shuffle(initial_state)
    rand_state.initial = tuple(initial_state)
    return rand_state

def make_rand_Ypuzzle():
    initial_state = [x for x in range(9)]
    random.shuffle(initial_state)
    rand_state = YPuzzle(initial_state)
    while rand_state.check_solvability(initial_state) != True:
        random.shuffle(initial_state)
    rand_state.initial = tuple(initial_state)
    return rand_state


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
    rm_count = 0            ## add the variable to count node has been removed 
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

def manhattan_8(node):

    ## The reference of the manhattan distance function is:
    ##      https://codereview.stackexchange.com/questions/110429/8-puzzle-using-a-and-manhattan-distance

    mhtd = 0
    state = list(node.state)
    for counter, value in enumerate(state):
        if value:
            index = value - 1
            mhtd = mhtd + abs(index//3 - counter//3) + abs(index%3 - counter%3)
    return mhtd
    

def manhattan_y(node):
    state = node.state
    index_goal = {0:[3,1], 1:[0,0], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}
    index_state = {}
    index = [[0,0], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2], [3,1]]

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(8):
        for j in range(2):
            mhd = abs(index_goal[i+1][j] - index_state[i+1][j]) + mhd

    return mhd



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
        
def display_y(state):
    for i in range (4):
        if i == 0:
            if state[0] == 0:
                print("*", end = '')
            else:
                print(state[0],'  ', end = '')
            if state[1] == 0:
                print("*", end = '')
            else:
                print(state[1], end = '')
        elif i == 3:
            if state[8] == 0:
                print('  *  ')
            else:
                print('  ', end = '')
                print(state[8], end = '')
                print('  ')
        else:
            for j in range (3):
                if state[2+3*(i-1)+j] == 0:
                    print("*", end = '')
                else:
                    print(state[(i-1)*3+2+j], end = '')
                if j != 2:
                    print(" ", end = '')
        print()
    


def max_8(node):
    temp = EightPuzzle(node.state)
    return max(manhattan_8(node),temp.h(node))

def max_y(node):
    temp = YPuzzle(node.state)
    return max(manhattan_y(node),temp.h(node))



######### Test Start #########
test_count = [1,2,3,4,5,6,7,8,9,10]

######### Test for 8-Puzzle #########

for i in range(10):
    x = make_rand_8puzzle()
    
    print('8-Puzzle Instance No.', test_count[i])
    print('The state is:', x.initial)
    print()
    display(x.initial)
    print()

    start_time = time.time()
    astar_h , astar_h_removed = astar_search(x)
    run_time_h = time.time() - start_time

    start_time = time.time()
    astar_m , astar_m_removed = astar_search(x,h = manhattan_8)
    run_time_m = time.time() - start_time

    start_time = time.time()
    astar_max , astar_max_removed = astar_search(x,h = max_8)
    run_time_max = time.time() - start_time

    print('For h algorithm', '\n','              total running time:', run_time_h)
    print('               lenth of solution:', len(astar_h.solution()))
    print('               total nodes removed:', astar_h_removed)

    print('For Manhattan algorithm', '\n','              total running time:', run_time_m)
    print('               lenth of solution:', len(astar_m.solution()))
    print('               total nodes removed:', astar_m_removed)

    print('For max of misplaced tile algorithm', '\n','              total running time:', run_time_max)
    print('               lenth of solution:', len(astar_max.solution()))
    print('               total nodes removed:', astar_max_removed)

    print('\n')
    print('-'*100)
    print('\n') 


######### Test for Y-Puzzle #########

print('+'*20, 'Y-Puzzle Test Start', '+'*20)

for i in range(10):
    x = make_rand_Ypuzzle()
    
    print('Y-Puzzle Instance No.', test_count[i],'\n')
    print('The state is:', x.initial)
    display_y(x.initial)

    start_time = time.time()
    astar_h , astar_h_removed = astar_search(x)
    run_time_h = time.time() - start_time

    start_time = time.time()
    astar_m , astar_m_removed = astar_search(x,h = manhattan_y)
    run_time_m = time.time() - start_time


    start_time = time.time()
    astar_max , astar_max_removed = astar_search(x,h = max_y)
    run_time_max = time.time() - start_time

    print('For h algorithm', '\n','              total running time:', run_time_h)
    print('               lenth of solution:', len(astar_h.solution()))
    print('               total nodes removed:', astar_h_removed)

    print('For Manhattan algorithm', '\n','              total running time:', run_time_m)
    print('               lenth of solution:', len(astar_m.solution()))
    print('               total nodes removed:', astar_m_removed)

    print('For max of misplaced tile algorithm', '\n','              total running time:', run_time_max)
    print('               lenth of solution:', len(astar_max.solution()))
    print('               total nodes removed:', astar_max_removed)


    print('\n')
    print('+'*100)
    print('\n')

######### Assignment 1 End #########
















