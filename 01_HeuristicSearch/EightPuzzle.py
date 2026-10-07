import random
import copy


class EightPuzzle:
    DESIRED_STATE = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]

    def __init__(self, puzzle_state = copy.deepcopy(DESIRED_STATE)):
        self.current_state = puzzle_state
        self.distance = None
        self.step_count = 0



    def is_solvable(self) -> bool:
        """
        Checks if the current puzzle state is solvable.
        :return: True if the current puzzle state is solvable. Otherwise False is returned.
        """
        # Check if all digits from 0 to 8 are present in the puzzle exactly one time
        flat_current_state = self.__flatten_current_state()
        for x in range(0,8):
            if not x in flat_current_state:
                return False
        
        # Check for inversions
        # One Inversion = ond digit that is in the wrong order from one digit
        if self.__count_inversions() % 2 == 0:
            return True
        
        return False

    def move_tile(self, direction) -> bool:
        """
        Moves the current puzzle state in the given direction.
        :param direction: Direction to move the empty space/zero-tile along. 0 = up. 1 = right. 2 = down. 3 = left.
        :return: True if it's a valid move. False if not.
        """
        
        # Convert direction to specific coloumn and rows directions that are easier to work with
        row_direction = 0
        col_direction = 0
        match direction:
            case 0:
                col_direction = -1
            case 1:
                row_direction = 1
            case 2:
                col_direction = 1
            case 3:
                row_direction = -1
            case _:
                return False
        
        # Find the position of the zero-tile
        zero_col = 0
        zero_row = 0
        for x in range(0,3):
            for y in range(0,3):
                if self.current_state [x][y] == 0:
                    zero_col = x
                    zero_row = y
        
        # Checks if the direction moves the zero-tile out of the bounds
        if not 0 <= zero_col + col_direction <= 2 or not 0 <= zero_row + row_direction <= 2:
            return False
        
        self.__swap_tiles(zero_col, zero_row, zero_col + col_direction, zero_row + row_direction)
        return True

    def randomize_current_state(self, iterations):
        """
        Randomizes the current puzzle state by moving the tiles around according to the rules of the puzzle.
        """
        # Move tiles in random direction. Only count an iteration when move is valid.
        random_choice_list = [0, 1, 2, 3]
        for x in range(0, iterations):
            random_direction = random.choice(random_choice_list)
            if not self.move_tile(random_direction):
                x -= 1
        return True
    
    def create_new_random_state(self):
        """
        Places the numbers of the eight puzzle in random locations, regardless of whether or not the outcome is a solvable eight puzzle.
        """
        random_choice_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for x in range(0,3):
            for y in range(0,3):
                random_choice = random.choice(random_choice_list)
                self.current_state[x][y] = random_choice
                random_choice_list.remove(random_choice)



    def __flatten_current_state(self):
        """
        Turns the current two dimensional puzzle state into a one dimensional list of numbers in the order they appear in.
        :return: The flattened puzzle state.
        """
        flat_puzzle_state = [None] * 9
        flat_position = 0
        for x in range(0,3):
            for y in range(0,3):
                flat_puzzle_state[flat_position] = self.current_state[x][y]
                flat_position += 1
        return flat_puzzle_state
    
    def __count_inversions(self):
        """
        Count the number of inversions in the current puzzle state.
        :return: The number of inversions.
        """
        simple_puzzle_state = self.__flatten_current_state()
        simple_puzzle_state.remove(0)
        inversion_counter = 0
        for x in range(0,8):
            for y in range(x+1,8):
                if simple_puzzle_state[x] > simple_puzzle_state[y]:
                    inversion_counter += 1
        return inversion_counter
    
    def __swap_tiles(self, first_x, first_y, second_x, second_y):
        """
        Swaps two tiles with each other on the given positions.
        :param first_x: Row coordinate of the first tile.
        :param first_y: Column coordinate of the first tile.
        :param second_x: Row coordinate of the second tile.
        :param second_y: Column coordinate of the second tile.
        """
        number_first = self.current_state [first_x][first_y]
        number_second = self.current_state [second_x][second_y]
        self.current_state [first_x][first_y] = number_second
        self.current_state [second_x][second_y] = number_first