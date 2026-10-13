import copy
from typing import List
from typing import Self
from EightPuzzle import EightPuzzle


class StarNode:
    def __init__(
        self,
        node_puzzle: EightPuzzle,
        parent_node: Self,
        parent_depth: int,
        heuristic: int,
    ):
        # The eight puzzle with the state of the puzzle this node has
        self.node_puzzle = node_puzzle
        self.parent_node = parent_node
        self.depth = parent_depth + 1
        self.heuristic = heuristic
        self.cost = self.__calculate_cost()

    def extract_children(self) -> List[Self]:
        """
        Expands the node, by adding a child node for each possible next move.
        :return: The children as a list.
        """
        next_possible_puzzle_states = []
        for x in range(0, 4):
            puzzle_option = copy.deepcopy(self.node_puzzle)
            if puzzle_option.move_tile(x):
                if self.parent_node == None:
                    next_possible_puzzle_states.append(puzzle_option)
                elif (
                    not puzzle_option.current_state
                    == self.parent_node.node_puzzle.current_state
                ):
                    # Appends the StarNode when it has a different puzzle state than the parent
                    next_possible_puzzle_states.append(puzzle_option)

        node_children = []
        for x in next_possible_puzzle_states:
            child_node = StarNode(x, self, self.depth, self.heuristic)
            node_children.append(child_node)

        return node_children

    def has_desired_state(self) -> bool:
        """
        Checks if the puzzle state of the node already is the desired state.
        :return: True, if the desired state is equal to this node's puzzle state.
        """
        return self.node_puzzle.current_state == self.node_puzzle.DESIRED_STATE

    def __calculate_cost(self):
        """
        Calculate the cost of the current node, with the given heuristic.
        :param heuristic: The heuristic. 0 = Hamming Distance. 1 = Manhattan Distance.
        :return: The cost as an integer.
        """
        match self.heuristic:
            case 0:
                # Hamming Distance
                return self.__get_hamming_distance() + self.depth
            case 1:
                # Manhattan Distance
                return self.__get_manhattan_distance() + self.depth
            case _:
                return 0

    def __get_hamming_distance(self):
        """
        Calculate the hamming distance for the node's eight puzzle state.
        :return: The hamming distance as an integer.
        """
        puzzle_state = self.node_puzzle.current_state
        hamming_distance = 0
        for x in range(0, 3):
            for y in range(0, 3):
                if not puzzle_state[x][y] == self.node_puzzle.DESIRED_STATE[x][y]:
                    hamming_distance += 1
        return hamming_distance

    def __get_manhattan_distance(self):
        """
        Calculate the manhattan distance for the node's eight puzzle state.
        :return: The manhattan distance as an integer.
        """
        manhattan_distance = 0
        for x in range(0, 3):
            for y in range(0, 3):
                y_in_desired = int(self.node_puzzle.current_state[x][y] % 3)
                x_in_desired = int(
                    (self.node_puzzle.current_state[x][y] - y_in_desired) / 3
                )
                manhattan_distance += abs(x - x_in_desired) + abs(y - y_in_desired)
        return manhattan_distance
