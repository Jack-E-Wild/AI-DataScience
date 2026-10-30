import copy
import csv
import random
import time
import statistics
import os
from datetime import datetime

from EightPuzzle import EightPuzzle
from StarSearch import StarSearch
from StarSearchGlobal import StarSearchGlobal

# Creates BenchmarkResults directory if it does not exist
def ensure_results_directory():
        os.makedirs("BenchmarkResults", exist_ok=True)

#generates a list of 100 solvable puzzles without duplicates
def generate_random_puzzles(amount=100):
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