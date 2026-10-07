import random
import copy
from EightPuzzle import EightPuzzle
import sys
import tracemalloc



def main():
    # Setting the Recursion Limit higher than the amount of possible states of the eight puzzle
    sys.setrecursionlimit(370000)
    puzzle_to_solve = EightPuzzle()
    puzzle_to_solve.randomize_current_state(100)
    print("")
    print("Hamming Distance")
    draw_puzzle_state(puzzle_to_solve)
    print("Solvable: ", puzzle_to_solve.is_solvable())
    print("Distance: ", get_hamming_distance(puzzle_to_solve))
    print("")
    print("Find next Hamming:")
    print("")
    
    print("")
    print("")
    print("Solving with Hamming:")
    print("")
    hamming_puzzle = EightPuzzle()
    hamming_puzzle.randomize_current_state(100)
    print("Puzzle at Start:")
    draw_puzzle_state(hamming_puzzle)
    
    tracemalloc.start()
    start_manhattan_method(hamming_puzzle)
    # Prints Mempry Usage with (current, peak)
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()
    
    draw_puzzle_state(hamming_puzzle)
    
    # ToDo:
    # Make a search tree object class instead of the methods below
    # Track Memory Usage / Number of Search Tree Nodes and Computation time for 100 solves each
    # Calculate the node tree in the way it is done in the lecture
    # >> Always find node with lowest cost and keep unopened nodes in memory
    # >> f(n) = g(n) + h(n)
    # >> f(n) ... estimated best path to goal
    # >> g(n) increases per 1 per node
    # >> h(n) distance to endstate for the new node



def start_hamming_method(puzzle):
    solving_step(puzzle, [], "hamming")
def start_manhattan_method(puzzle):
    solving_step(puzzle, [], "manhattan")

def solving_step(puzzle, excluded_states, method):
    # Add the current puzzle state to the excluded states
    excluded_states.append(puzzle.current_state)
    
    # Create a list of possible directions to move the given puzzle in
    options_next_state = []
    for x in range(0,4):
        puzzle_option = copy.deepcopy(puzzle)
        if puzzle_option.move_tile(x):
            if not puzzle_option.current_state in excluded_states:
                options_next_state.append(puzzle_option)
    
    # Set hamming or manhattan distance for all possible options
    for x in options_next_state:
        if method == "hamming":
            x.distance = get_hamming_distance(x)
        else:
            x.distance = get_manhattan_distance(x)
    
    # Sort by distance
    options_next_state.sort(key=lambda x: x.distance)
    
    for x in options_next_state:
        puzzle.step_count += 1
        print(puzzle.step_count)
        draw_puzzle_state(x)
        print("")
        if x.current_state == x.DESIRED_STATE:
            puzzle.current_state = x.current_state
            return True
        else:
            puzzle_for_exclusion = copy.deepcopy(puzzle)
            puzzle.current_state = x.current_state
            # Here is where a new node gets added/opened in this search tree (maybe this can be solved more elegantly?)
            if solving_step(puzzle, excluded_states, method) == True:
                return True
    
    return False

def get_hamming_distance(puzzle):
    """
    Calculate the hamming distance for the state of the given puzzle.
    :param puzzle: The puzzle containing the puzzle state.
    :return: The hamming distance as a number.
    """
    puzzle_state = puzzle.current_state
    hamming_distance = 0
    for x in range(0,3):
        for y in range(0,3):
            if not puzzle_state [x][y] == puzzle.DESIRED_STATE [x][y]:
                hamming_distance += 1
    return hamming_distance

def get_manhattan_distance(puzzle):
    manhattan_distance = 0
    for x in range(0,3):
        for y in range(0,3):
            y_in_desired = int(puzzle.current_state [x][y] %3)
            x_in_desired = int((puzzle.current_state [x][y] - y_in_desired)/3)
            manhattan_distance += abs(x-x_in_desired) + abs(y-y_in_desired)
    return manhattan_distance



def draw_puzzle_state(puzzle):
    """
    Prints the given 8-puzzle state on the console.
    :param puzzle_state: The given state for the 8-puzzle that has to be drawn.
    """
    puzzle_state = puzzle.current_state
    if not puzzle_state is None:
        print(check_if_zero(puzzle_state[0][0]), check_if_zero(puzzle_state[0][1]), check_if_zero(puzzle_state[0][2]))
        print(check_if_zero(puzzle_state[1][0]), check_if_zero(puzzle_state[1][1]), check_if_zero(puzzle_state[1][2]))
        print(check_if_zero(puzzle_state[2][0]), check_if_zero(puzzle_state[2][1]), check_if_zero(puzzle_state[2][2]))
    else:
        print("Puzzle is None")

def check_if_zero(number_to_check):
    """
    Checks if the given number is 0 and colors it red if it is.
    :param number_to_check: The number to check.
    :return: Either the number 0 in red or the given number, if it isn't 0.
    """
    if number_to_check == 0:
        return "\033[91m0\033[0m"
    else:
        return number_to_check




# Run main when opening the script
if __name__=="__main__":
    main()