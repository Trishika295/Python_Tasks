from prime_analyzer import (
    is_prime,
    generate_primes,
    analyze_number,
    show_algorithm
)


def print_header():

    print("\n" + "=" * 65)
    print("                  PRIME NUMBER ANALYZER")
    print("=" * 65)

    print("Check prime numbers and generate primes within a range.")


def check_prime():

    print("\n" + "-" * 65)
    print("                    PRIME NUMBER CHECKER")
    print("-" * 65)

    while True:

        user_input = input(
            "\nEnter a number to check "
            "(or type 'back' to return): "
        ).strip()

        if user_input.lower() == "back":
            return

        try:

            number = int(user_input)

            result = analyze_number(number)

            print("\nResult:")

            if result["prime"]:
                print(f"✓ {result['message']}")
            else:
                print(f"✗ {result['message']}")

        except ValueError:

            print("\nInvalid input.")
            print("Please enter a valid integer.")


def generate_prime_range():

    print("\n" + "-" * 65)
    print("                    PRIME RANGE GENERATOR")
    print("-" * 65)

    while True:

        start_input = input(
            "\nEnter starting number "
            "(or type 'back' to return): "
        ).strip()

        if start_input.lower() == "back":
            return

        try:

            start = int(start_input)

            break

        except ValueError:

            print("\nInvalid starting number.")
            print("Please enter a valid integer.")

    while True:

        end_input = input(
            "Enter ending number: "
        ).strip()

        try:

            end = int(end_input)

            break

        except ValueError:

            print("\nInvalid ending number.")
            print("Please enter a valid integer.")

    # Generate primes
    primes = generate_primes(start, end)

    # Display actual range used
    if start > end:
        start, end = end, start

    print("\n" + "=" * 65)
    print(f"Prime numbers between {start} and {end}")
    print("=" * 65)

    if primes:

        print("\nPrime Numbers:")

        # Display primes in groups of 10
        for index in range(0, len(primes), 10):

            group = primes[index:index + 10]

            print("   ".join(map(str, group)))

        print(f"\nTotal prime numbers found: {len(primes)}")

    else:

        print("\nNo prime numbers were found in this range.")

    print("=" * 65)


def show_examples():

    print("\n" + "=" * 65)
    print("                     EXAMPLES")
    print("=" * 65)

    examples = [
        0,
        1,
        2,
        3,
        4,
        10,
        17,
        25,
        97,
        100
    ]

    for number in examples:

        if is_prime(number):
            result = "Prime"
        else:
            result = "Not Prime"

        print(f"{number:>5}  →  {result}")

    print("=" * 65)


def main():

    while True:

        print_header()

        print("\n")
        print("1. Check whether a number is prime")
        print("2. Generate prime numbers within a range")
        print("3. Show algorithm explanation")
        print("4. Show example test cases")
        print("5. Exit")

        print("\n" + "-" * 65)

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":

            check_prime()

        elif choice == "2":

            generate_prime_range()

        elif choice == "3":

            show_algorithm()

        elif choice == "4":

            show_examples()

        elif choice == "5":

            print("\n" + "=" * 65)
            print("Thank you for using Prime Number Analyzer!")
            print("=" * 65)

            break

        else:

            print("\nInvalid choice.")
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()