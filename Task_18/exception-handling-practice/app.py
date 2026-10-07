"""
Practice Exception Handling
Python Programming Mini Project

This project demonstrates practical exception handling using:
try, except, else, and finally.

Handled exceptions:
1. ValueError
2. ZeroDivisionError
3. KeyError
4. IndexError
5. TypeError
6. FileNotFoundError
"""


def invalid_numeric_input():
    """Demonstrate handling of invalid numeric input."""

    print("\n--- Invalid Numeric Input ---")

    try:
        number = int(input("Enter a whole number: "))

    except ValueError:
        print("Error: Invalid input. Please enter a valid whole number.")

    else:
        print(f"Success: You entered {number}.")

    finally:
        print("Numeric input operation completed.")


def division_by_zero():
    """Demonstrate handling of division by zero."""

    print("\n--- Division by Zero ---")

    try:
        numerator = float(input("Enter the numerator: "))
        denominator = float(input("Enter the denominator: "))

        result = numerator / denominator

    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")

    except ValueError:
        print("Error: Please enter valid numeric values.")

    else:
        print(f"Result: {result}")

    finally:
        print("Division operation completed.")


def missing_dictionary_value():
    """Demonstrate handling of a missing dictionary key."""

    print("\n--- Missing Dictionary Value ---")

    student = {
        "name": "Trishika",
        "course": "Python Programming",
        "score": 90
    }

    print("Available student information:")
    print(student)

    key = input("Enter the key you want to access: ")

    try:
        value = student[key]

    except KeyError:
        print(f"Error: The key '{key}' does not exist in the student record.")

    else:
        print(f"Value: {value}")

    finally:
        print("Dictionary operation completed.")


def invalid_list_index():
    """Demonstrate handling of an invalid list index."""

    print("\n--- Invalid List Index ---")

    subjects = [
        "Python",
        "Database Management",
        "Data Structures",
        "Web Development"
    ]

    print("Available subjects:")
    for index, subject in enumerate(subjects):
        print(f"{index}: {subject}")

    try:
        index = int(input("Enter the index you want to access: "))
        subject = subjects[index]

    except ValueError:
        print("Error: Index must be a whole number.")

    except IndexError:
        print("Error: The selected index does not exist.")

    else:
        print(f"Selected subject: {subject}")

    finally:
        print("List operation completed.")


def invalid_data_type():
    """Demonstrate handling of an invalid data type operation."""

    print("\n--- Invalid Data Type Operation ---")

    try:
        number = 10
        text = "Python"

        result = number + text

    except TypeError:
        print("Error: These data types cannot be added together.")

    else:
        print(f"Result: {result}")

    finally:
        print("Data type operation completed.")


def missing_file():
    """Demonstrate handling of a missing file."""

    print("\n--- Missing File ---")

    filename = input("Enter the file name to open: ")

    try:
        with open(filename, "r") as file:
            content = file.read()

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")

    except PermissionError:
        print(f"Error: Permission denied while accessing '{filename}'.")

    else:
        print("\nFile contents:")
        print(content)

    finally:
        print("File operation completed.")


def display_exception_explanation():
    """Display explanations of the exceptions used in the project."""

    print("\n--- Exception Explanations ---")

    explanations = {
        "ValueError":
            "Occurs when a function receives a value of the correct type "
            "but an inappropriate value.",

        "ZeroDivisionError":
            "Occurs when a number is divided by zero.",

        "KeyError":
            "Occurs when a dictionary key being accessed does not exist.",

        "IndexError":
            "Occurs when a list or sequence index is outside its valid range.",

        "TypeError":
            "Occurs when an operation is performed on incompatible data types.",

        "FileNotFoundError":
            "Occurs when a program attempts to open a file that does not exist."
    }

    for exception_name, explanation in explanations.items():
        print(f"\n{exception_name}:")
        print(explanation)


def display_menu():
    """Display the main menu."""

    print("\n" + "=" * 55)
    print("       PYTHON EXCEPTION HANDLING PRACTICE")
    print("=" * 55)

    print("1. Invalid Numeric Input")
    print("2. Division by Zero")
    print("3. Missing Dictionary Value")
    print("4. Invalid List Index")
    print("5. Invalid Data Type Operation")
    print("6. Missing File")
    print("7. Exception Explanations")
    print("8. Exit")

    print("=" * 55)


def main():
    """Run the exception handling demonstration program."""

    while True:

        display_menu()

        try:
            choice = int(input("Enter your choice: "))

        except ValueError:
            print("Error: Please enter a number between 1 and 8.")
            continue

        if choice == 1:
            invalid_numeric_input()

        elif choice == 2:
            division_by_zero()

        elif choice == 3:
            missing_dictionary_value()

        elif choice == 4:
            invalid_list_index()

        elif choice == 5:
            invalid_data_type()

        elif choice == 6:
            missing_file()

        elif choice == 7:
            display_exception_explanation()

        elif choice == 8:
            print("\nThank you for using the Exception Handling Practice.")
            print("Program terminated safely.")
            break

        else:
            print("Error: Please select a valid option from 1 to 8.")


if __name__ == "__main__":
    main()