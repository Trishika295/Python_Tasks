import math


def is_prime(number):
    """
    Check whether a number is prime.

    Returns:
        True  -> number is prime
        False -> number is not prime
    """

    # Numbers less than 2 are not prime
    if number < 2:
        return False

    # 2 is the only even prime number
    if number == 2:
        return True

    # Other even numbers are not prime
    if number % 2 == 0:
        return False

    # Check only odd divisors up to square root of number
    limit = int(math.sqrt(number))

    for divisor in range(3, limit + 1, 2):

        if number % divisor == 0:
            return False

    return True


def generate_primes(start, end):
    """
    Generate all prime numbers within a given range.

    The range includes both start and end.
    """

    # Handle reversed ranges
    if start > end:
        start, end = end, start

    primes = []

    for number in range(start, end + 1):

        if is_prime(number):
            primes.append(number)

    return primes


def analyze_number(number):
    """
    Analyze a number and return its prime status.
    """

    if is_prime(number):

        return {
            "number": number,
            "prime": True,
            "message": f"{number} is a prime number."
        }

    return {
        "number": number,
        "prime": False,
        "message": f"{number} is not a prime number."
    }


def show_algorithm():

    print("\n" + "=" * 60)
    print("                 PRIME CHECKING ALGORITHM")
    print("=" * 60)

    print("""
1. A number less than 2 is not prime.

2. The number 2 is the only even prime number.

3. Other even numbers are not prime.

4. For odd numbers, only odd divisors are checked.

5. Divisibility checks are performed only up to √n.

6. If no divisor is found, the number is prime.
""")

    print("Complexity:")
    print("- Time Complexity for one number : O(√n)")
    print("- Space Complexity              : O(1)")

    print("\nRange Generation:")
    print("- The is_prime() function is applied to each number")
    print("  in the specified range.")

    print("=" * 60)