import copy
from EightPuzzle import EightPuzzle
from StarSearch import StarSearch
import time



def main():
    for x in range(0,10):
        # Example of creating a random eight puzzle for both heuristics
        eight_puzzle_hamming = EightPuzzle()
        eight_puzzle_hamming.randomize_current_state(20)
        eight_puzzle_manhattan = copy.deepcopy(eight_puzzle_hamming)
        print(x, " - Eight Puzzle to solve:")
        draw_puzzle_state(eight_puzzle_hamming)
        print("-------")

        # Example of creating an eight puzzle, randomizing it
        # And solving it with Hamming Distance heuristic
        print("Hamming:")
        start_hamming = time.time()
        star_search_hamming = StarSearch(eight_puzzle_hamming)
        star_search_hamming.solve_puzzle_heuristically(0)
        end_hamming = time.time()
        length_hamming = end_hamming - start_hamming
        print("\033[2A")
        print("Expanded Nodes: ", len(star_search_hamming.expanded_nodes))
        print("Time it took: ", length_hamming, " Seconds")

        # Example of creating an eight puzzle, randomizing it
        # And solving it with Manhattan Distance heuristic
        print("Manhattan:")
        start_manhattan = time.time()
        star_search_manhattan = StarSearch(eight_puzzle_manhattan)
        star_search_manhattan.solve_puzzle_heuristically(1)
        end_manhattan = time.time()
        length_manhattan = end_manhattan - start_manhattan
        print("\033[2A")
        print("Expanded Nodes: ", len(star_search_manhattan.expanded_nodes))
        print("Time it took: ", length_manhattan, " Seconds")

        print()




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
