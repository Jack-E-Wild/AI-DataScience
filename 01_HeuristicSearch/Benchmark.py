import copy
import csv
import time
import statistics
import os
from datetime import datetime

from EightPuzzle import EightPuzzle
from StarSearch import StarSearch
from StarSearchGlobal import StarSearchGlobal

"""
This module provides benchmarking functionality for evaluating and 
comparing different A* search implementations and heuristic functions.

It generates puzzle instances, executes search algorithms, measures
their performance, calculates summary statistics, and exports the
results to CSV files.
"""

# Creates BenchmarkResults directory if it does not exist
def ensure_results_directory():
    """
    Creates the BenchmarkResults directory if it does not already exist.
    """
    os.makedirs("BenchmarkResults", exist_ok=True)

#generates a list of 100 solvable puzzles without duplicates
def generate_random_puzzles(amount=100):
    """
    Generates a specified number of unique, solvable Eight Puzzle states.

    :param amount: Number of unique puzzles to generate.
    :return list: A list containing the generated EightPuzzle instances.
    """
    puzzles = []
    #uses set() to sort out duplicates
    seen_states = set()

    while len(puzzles) < amount:
        puzzle = EightPuzzle()
        puzzle.create_new_random_state()

        if not puzzle.is_solvable():
            continue

        #array gets changed with tuple so set can check for duplicates
        state_key = tuple(
            number
            for row in puzzle.current_state
            for number in row
        )

        if state_key in seen_states:
            continue

        seen_states.add(state_key)
        puzzles.append(copy.deepcopy(puzzle))

    return puzzles


def benchmark_puzzle(puzzle, puzzle_id, search_class, version):
    """
    Executes a benchmark for a single puzzle using two heuristic functions.

    :param   puzzle: Puzzle instance to solve.
    :param   puzzle_id: Identifier of the puzzle.
    :param   search_class: A* search implementation to benchmark.
    :param   version: Name identifying the search implementation.


    :return list: Benchmark results for both heuristic executions.
    """

    results = []

    heuristic_names = {
        0: "Hamming",
        1: "Manhattan"
    }

    # Run the search with both heuristics
    for heuristic in [0, 1]:

        # Create an independent copy of the puzzle
        puzzle_copy = copy.deepcopy(puzzle)

        # Initialize the selected search algorithm
        search = search_class(puzzle_copy)

        # Start measuring execution time
        start_time = time.perf_counter()

        # Solve the puzzle
        solved = search.solve_puzzle_heuristically(heuristic)

        # Stop measuring execution time
        end_time = time.perf_counter()

        # Calculate runtime and count expanded nodes
        runtime = end_time - start_time
        expanded_nodes = len(search.expanded_nodes)

        # Store the results
        results.append({
            "puzzle_id": puzzle_id,
            "version": version,
            "heuristic": heuristic_names[heuristic],
            "runtime_s": runtime,
            "expanded_nodes": expanded_nodes,
            "solved": solved
        })

        print(version, "-", heuristic_names[heuristic])
        print("Runtime:", runtime, "seconds")
        print("Expanded nodes:", expanded_nodes)
        print()

    return results

def save_raw_results(results):
    """
    Saves the individual benchmark results to a timestamped CSV file.

    :param results: List containing the individual benchmark results.
    """
    ensure_results_directory()

    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Define the output filename | BenchmarkResults must exist, otherwise program won't work
    filename = (
        f"BenchmarkResults/raw_results_{timestamp}.csv"
    )

    # Define the column names
    fieldnames = [
        "puzzle_id",
        "version",
        "heuristic",
        "runtime_s",
        "expanded_nodes",
        "solved"
    ]

    # Write the results into a CSV file
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for result in results:
            formatted_result = result.copy()

            formatted_result["runtime_s"] = f"{result['runtime_s']:.4f}"

            writer.writerow(formatted_result)

    print("Raw results saved to", filename)


def calculate_summary(results):
    """
    Calculates summary statistics for the benchmark results.
    :param results: List containing the individual benchmark results.

    :return list: Summary statistics for each available combination
                  of search implementation and heuristic.
    """
    summary = []

    # Get all algorithm and heuristic combinations
    combinations = [
        ("Original", "Hamming"),
        ("Original", "Manhattan"),
        ("Global", "Hamming"),
        ("Global", "Manhattan")
    ]

    for version, heuristic in combinations:

        # Select results for the current combination
        selected_results = [
            result for result in results
            if result["version"] == version
            and result["heuristic"] == heuristic
            and result["solved"]
        ]

        # Extract runtime and expanded nodes
        runtimes = [
            result["runtime_s"] for result in selected_results
        ]

        expanded_nodes = [
            result["expanded_nodes"] for result in selected_results
        ]

        # Skip combinations without any results
        if not selected_results:
            continue

        # Calculate averages
        average_runtime = statistics.mean(runtimes)
        average_expanded_nodes = statistics.mean(expanded_nodes)

        # Calculate standard deviations if at least two measurements exist
        if len(runtimes) >= 2:
            std_runtime = statistics.stdev(runtimes)
            std_expanded_nodes = statistics.stdev(expanded_nodes)
        else:
            std_runtime = 0
            std_expanded_nodes = 0

        summary.append({
            "version": version,
            "heuristic": heuristic,
            "average_runtime_s": f"{average_runtime:.4f}",
            "std_runtime_s": f"{std_runtime:.4f}",
            "average_expanded_nodes": f"{average_expanded_nodes:.2f}",
            "std_expanded_nodes": f"{std_expanded_nodes:.2f}"
        })

    return summary

def save_summary(summary):
    """
    Saves the calculated benchmark summary to a timestamped CSV file.

    :param summary: List containing the calculated summary statistics.
    """
    ensure_results_directory()
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Define the output filename
    filename = (
        f"BenchmarkResults/summary_{timestamp}.csv"
    )

    # Define the column names
    fieldnames = [
        "version",
        "heuristic",
        "average_runtime_s",
        "std_runtime_s",
        "average_expanded_nodes",
        "std_expanded_nodes"
    ]

    # Write the summary into a CSV file
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(summary)

    print("Summary saved to", filename)

# Print the current puzzle state
def print_puzzle(puzzle):
    """
    Prints the current Eight Puzzle state in a formatted grid.
    :param puzzle: Puzzle instance to display.
    """

    for row in puzzle.current_state:
        print("+---+---+---+")
        print("|", end="")

        for number in row:
            if number == 0:
                print("   |", end="")
            else:
                print(f" {number} |", end="")

        print()

    print("+---+---+---+")


#TESTING
def run_randomize_test(amount, iterations):
    """
    Runs benchmarks using puzzle states created through random moves and saves results to a CSV file.
    :param amount: Number of puzzles to generate.
    :param iterations: Number of random move iterations per puzzle.
    """

    # Store all benchmark results
    all_results = []

    # Generate and benchmark the requested number of puzzles
    for index in range(1, amount + 1):
        print("================================")
        print("Puzzle", index, "of", amount)
        print("================================")

        # Create a new puzzle
        puzzle = EightPuzzle()

        # Randomize the puzzle using the requested number of iterations
        puzzle.randomize_current_state(iterations)

        # Display the puzzle before benchmarking
        print("Puzzle state:")
        print_puzzle(puzzle)


        # Run the benchmark using StarSearch
        results = benchmark_puzzle(
            puzzle,
            index,
            StarSearch,
            "Original"
        )

        all_results.extend(results)

    # Save raw results
    save_raw_results(all_results)

    # Calculate and save summary
    summary = calculate_summary(all_results)
    save_summary(summary)

    print("Benchmark completed!")
    print("Total measurements:", len(all_results))


def run_random_puzzles_test(amount):
    """
    Runs benchmarks using randomly generated solvable puzzle states and saves results to a CSV file.
    :param amount: Number of puzzles to generate and benchmark.
    """
    # Store all benchmark results
    all_results = []

    # Generate the requested number of random puzzles
    puzzles = generate_random_puzzles(amount)

    # Benchmark each generated puzzle
    for index, puzzle in enumerate(puzzles, start=1):
        print("================================")
        print("Puzzle", index, "of", amount)
        print("================================")

        # Display the puzzle before benchmarking
        print("Puzzle state:")
        print_puzzle(puzzle)

        # Run the benchmark using StarSearch
        results = benchmark_puzzle(
            puzzle,
            index,
            StarSearch,
            "Original"
        )

        all_results.extend(results)

    # Save raw results
    save_raw_results(all_results)

    # Calculate and save summary
    summary = calculate_summary(all_results)
    save_summary(summary)

    print("Benchmark completed!")
    print("Total measurements:", len(all_results))


def run_comparison_test():
    """
    Compares the original and global A* search implementations and saves results to a CSV file.
    """
    # Store all benchmark results
    all_results = []

    # Generate five random puzzles
    puzzles = generate_random_puzzles(5)

    # Benchmark each puzzle
    for index, puzzle in enumerate(puzzles, start=1):
        print("================================")
        print("Puzzle", index, "of", len(puzzles))
        print("================================")

        # Display the puzzle before benchmarking
        print("Puzzle state:")
        print_puzzle(puzzle)

        # Run the original search algorithm
        original_results = benchmark_puzzle(
            puzzle,
            index,
            StarSearch,
            "Original"
        )
        all_results.extend(original_results)

        # Run the global search algorithm
        global_results = benchmark_puzzle(
            puzzle,
            index,
            StarSearchGlobal,
            "Global"
        )
        all_results.extend(global_results)

    # Save raw results
    save_raw_results(all_results)

    # Calculate and save summary
    summary = calculate_summary(all_results)
    save_summary(summary)

    print("Benchmark completed!")
    print("Total measurements:", len(all_results))