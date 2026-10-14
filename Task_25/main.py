
"""
Python Utility Toolkit
Example application demonstrating utility_module.py.
"""

from pathlib import Path

from utility_module import (
    is_valid_email,
    is_valid_phone,
    is_number,
    format_name,
    format_currency,
    format_text,
    calculate_percentage,
    calculate_average,
    calculate_total,
    file_exists,
    read_text_file,
    write_text_file,
)


BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DIR = BASE_DIR / "sample_files"


def validation_demo():
    """Demonstrate validation functions."""
    print("\n--- Validation Utilities ---")

    email = input("Enter an email address: ").strip()
    phone = input("Enter a 10-digit phone number: ").strip()
    number = input("Enter a number: ").strip()

    print("Valid email:", is_valid_email(email))
    print("Valid phone:", is_valid_phone(phone))
    print("Valid number:", is_number(number))


def formatting_demo():
    """Demonstrate formatting functions."""
    print("\n--- Formatting Utilities ---")

    name = input("Enter a name: ")
    text = input("Enter a sentence: ")

    print("Formatted name:", format_name(name))
    print("Formatted text:", format_text(text))

    try:
        amount = float(input("Enter an amount in rupees: "))

        if not is_number(str(amount)):
            print("Please enter a finite amount.")
            return

        print("Formatted currency:", format_currency(amount))

    except ValueError:
        print("Please enter a valid numeric amount.")


def calculation_demo():
    """Demonstrate calculation functions."""
    print("\n--- Calculation Utilities ---")

    try:
        raw_values = input(
            "Enter numbers separated by commas: "
        )

        values = [float(item.strip()) for item in raw_values.split(",")]

        if not values or not all(is_number(str(n)) for n in values):
            print("Please enter finite numbers.")
            return

        print("Total:", calculate_total(values))
        print("Average:", round(calculate_average(values), 2))

        value = float(input("Enter a value for percentage: "))
        total = float(input("Enter the total value: "))

        if not is_number(str(value)) or not is_number(str(total)):
            print("Please enter finite numbers.")
            return

        percentage = calculate_percentage(value, total)
        print(f"Percentage: {percentage:.2f}%")

    except ValueError as error:
        print("Invalid input:", error)


def file_demo():
    """Demonstrate file creation, writing, checking, and reading."""
    print("\n--- File Utilities ---")

    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    file_path = SAMPLE_DIR / "example.txt"

    content = (
        "Python Utility Toolkit\n"
        "This file demonstrates reusable file functions.\n"
        "Modules make code easier to maintain and reuse.\n"
    )

    try:
        write_text_file(str(file_path), content)
        print("File created:", file_path.name)
        print("File exists:", file_exists(str(file_path)))
        print("\nFile contents:")
        print(read_text_file(str(file_path)))

    except OSError as error:
        print("File operation failed:", error)


def main():
    """Display the menu and run the selected demonstration."""
    while True:
        print("\n" + "=" * 42)
        print("       PYTHON UTILITY TOOLKIT")
        print("=" * 42)
        print("1. Validation utilities")
        print("2. Formatting utilities")
        print("3. Calculation utilities")
        print("4. File utilities")
        print("5. Run all demonstrations")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            validation_demo()
        elif choice == "2":
            formatting_demo()
        elif choice == "3":
            calculation_demo()
        elif choice == "4":
            file_demo()
        elif choice == "5":
            validation_demo()
            formatting_demo()
            calculation_demo()
            file_demo()
        elif choice == "0":
            print("Thank you for using Python Utility Toolkit!")
            break
        else:
            print("Invalid choice. Please select an option from 0 to 5.")


if __name__ == "__main__":
    main()
