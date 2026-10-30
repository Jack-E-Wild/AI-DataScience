import copy
from StarNode import StarNode
from EightPuzzle import EightPuzzle


class StarSearchGlobal:
    def __init__(self, puzzle_to_solve: EightPuzzle):
        self.initial_puzzle = copy.deepcopy(puzzle_to_solve)
        self.expanded_nodes = []
        self.not_expanded_nodes = []
        # Store expanded puzzle states and their lowest known path cost
        self.closed_set = {}
        self.solved = False

    def get_state_key(self, puzzle):
        # Convert puzzle array into a flat tuple
        return tuple(
            number
            for row in puzzle.current_state
            for number in row
        )

    def solve_puzzle_heuristically(self, heuristic):
        """
        Uses StarSearch.py as base and adds a global set of already checked states, so the same state won't get checked again.
        Goal: shorten time for hamming search.
        :param heuristic: The heuristic the search algorithm uses. 0 = Hamming Distance. 1 = Manhattan Distance.
        :return:  True if the puzzle was successfully solved, otherwise False.
        """
        root_node = StarNode(self.initial_puzzle, None, -1, heuristic)

        # Check whether the initial state is already the goal state
        if root_node.has_desired_state():
            self.solved = True
            return True

        for x in root_node.extract_children():
            self.not_expanded_nodes.append(x)
        self.expanded_nodes.append(root_node)
        # Add the initial puzzle state to the closed set
        root_key = self.get_state_key(root_node.node_puzzle)
        self.closed_set[root_key] = root_node.depth

        while self.solved == False and self.not_expanded_nodes:
            current_node = min(self.not_expanded_nodes, key=lambda x: x.cost)

            current_key = self.get_state_key(current_node.node_puzzle)

            # Skip the node if a better path to this state was already expanded
            if current_key in self.closed_set:
                if self.closed_set[current_key] <= current_node.depth:
                    self.not_expanded_nodes.remove(current_node)
                    continue

            if current_node.has_desired_state():
                self.solved = True
            else:
                self.not_expanded_nodes.remove(current_node)
                self.expanded_nodes.append(current_node)

                # Store the current state and its depth
                self.closed_set[current_key] = current_node.depth

                for x in current_node.extract_children():
                    child_key = self.get_state_key(x.node_puzzle)

                    # Skip children that were already reached through a better path
                    if child_key in self.closed_set:
                        if self.closed_set[child_key] <= x.depth:
                            continue

                    # Check whether the child state is already in the open list
                    existing_node = None

                    for node in self.not_expanded_nodes:
                        if self.get_state_key(node.node_puzzle) == child_key:
                            existing_node = node
                            break

                    # Keep the existing node if it has a better or equal path
                    if existing_node is not None:
                        if existing_node.depth <= x.depth:
                            continue

                        # Remove the existing node if the new path is shorter
                        self.not_expanded_nodes.remove(existing_node)

                    # Add the new or improved node to the open list
                    self.not_expanded_nodes.append(x)

        return self.solved

