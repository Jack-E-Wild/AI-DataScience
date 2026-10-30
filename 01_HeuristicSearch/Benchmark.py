import copy
import csv
import random
import time
import statistics
from datetime import datetime
from EightPuzzle import EightPuzzle
from StarSearch import StarSearch
from StarSearchGlobal import StarSearchGlobal

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

        # Calculate averages and standard deviations
        summary.append({
            "version": version,
            "heuristic": heuristic,
            "average_runtime_s": f"{statistics.mean(runtimes):.4f}",
            "std_runtime_s": f"{statistics.stdev(runtimes):.4f}",
            "average_expanded_nodes": f"{statistics.mean(expanded_nodes):.2f}",
            "std_expanded_nodes": f"{statistics.stdev(expanded_nodes):.2f}"
        })

    return summary

def save_summary(summary):
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


if __name__ == "__main__":

    # Generate three solvable puzzles
    puzzles = generate_random_puzzles(2)

    all_results = []

    # Test each puzzle with both search algorithms
    for index, puzzle in enumerate(puzzles, start=1):

        print("================================")
        print("Puzzle", index, "of", len(puzzles))
        print("================================")

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

    # Save all benchmark results
    save_raw_results(all_results)
    # Calculate and save summary results
    summary = calculate_summary(all_results)
    save_summary(summary)


    print("Benchmark completed!")
    print("Total measurements:", len(all_results))