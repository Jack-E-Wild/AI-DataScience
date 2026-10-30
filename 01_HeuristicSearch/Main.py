from Benchmark import (
    run_randomize_test,
    run_random_puzzles_test,
    run_comparison_test
)


def main():
    print("================================")
    print("       8-Puzzle Benchmark")
    print("================================")
    print("1 - Randomize Current State")
    print("2 - Generate Random Puzzles")
    print("3 - Compare StarSearch and StarSearchGlobal")
    print("================================")

    choice = input("Select a test (1-3): ")

    match choice:
        case "1":
            amount = int(input("How many puzzles should be tested? "))
            iterations = int(input("How many random iterations per puzzle? "))

            run_randomize_test(amount, iterations)

        case "2":
            amount = int(input("How many puzzles should be tested? "))

            run_random_puzzles_test(amount)

        case "3":
            print("================================")
            print("Compares StarSearch and StarSearchGlobal with 5 random puzzles")
            print("================================")
            run_comparison_test()

        case _:
            print("Invalid selection.")


# Run main when opening the script
if __name__=="__main__":
    main()
