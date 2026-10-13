import copy
from StarNode import StarNode
from EightPuzzle import EightPuzzle


class StarSearch:
    def __init__(self, puzzle_to_solve: EightPuzzle):
        self.initial_puzzle = copy.deepcopy(puzzle_to_solve)
        self.expanded_nodes = []
        self.not_expanded_nodes = []
        self.solved = False

    def solve_puzzle_heuristically(self, heuristic):
        """
        Solves the puzzle using a star search and the given heuristic.
        :param heuristic: The heuristic the search algorithm uses. 0 = Hamming Distance. 1 = Manhattan Distance.
        :return: Returns True when puzzle has been succesfully solved. Returns False when it is already solved or couldn't be solved for other reasons.
        """
        # Create a root node and add its children to the not expanded nodes
        root_node = StarNode(self.initial_puzzle, None, -1, heuristic)
        for x in root_node.extract_children():
            self.not_expanded_nodes.append(x)
        self.expanded_nodes.append(root_node)

        while self.solved == False:
            # Get the not expanded node with the lowest value so far
            current_node = min(self.not_expanded_nodes, key=lambda x: x.cost)
            if current_node.has_desired_state():
                # The eight puzzle of the current node has the desired state
                self.solved = True
            else:
                # The current node gets transfered to the expanded nodes
                self.not_expanded_nodes.remove(current_node)
                self.expanded_nodes.append(current_node)

                for x in current_node.extract_children():
                    self.not_expanded_nodes.append(x)
            print("Expanded Nodes: ", len(self.expanded_nodes))
            print("\033[2A")
        print("\r")
        return self.solved
