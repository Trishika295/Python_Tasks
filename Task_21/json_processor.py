
import json
from pathlib import Path


# Get the JSON file from the same folder as this script
DATA_FILE = Path(__file__).with_name("data.json")


def load_data():
    """Load and validate employee records from a JSON file."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("Error: The JSON root must be an object.")
            return []

        employees = data.get("employees")

        if not isinstance(employees, list):
            print("Error: 'employees' must be a list.")
            return []

        required_keys = {
            "EmployeeID", "Name", "Department", "Salary"
        }

        valid_employees = []

        for index, employee in enumerate(employees, start=1):
            if not isinstance(employee, dict):
                print(f"Skipping record {index}: Not a JSON object.")
                continue

            if not required_keys.issubset(employee.keys()):
                print(f"Skipping record {index}: Missing required keys.")
                continue

            if not isinstance(employee["Name"], str) or not employee["Name"].strip():
                print(f"Skipping record {index}: Invalid name.")
                continue

            if not isinstance(employee["Department"], str) or not employee["Department"].strip():
                print(f"Skipping record {index}: Invalid department.")
                continue

            if (
                isinstance(employee["Salary"], bool)
                or not isinstance(employee["Salary"], (int, float))
                or employee["Salary"] < 0
            ):
                print(f"Skipping record {index}: Invalid salary.")
                continue

            if (
                isinstance(employee["EmployeeID"], bool)
                or not isinstance(employee["EmployeeID"], int)
            ):
                print(f"Skipping record {index}: Invalid EmployeeID.")
                continue

            valid_employees.append(employee)

        return valid_employees

    except FileNotFoundError:
        print("Error: data.json was not found.")
    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON format: {error}")
    except OSError as error:
        print(f"Error reading file: {error}")

    return []


def display_employees(employees):
    """Display employee records in a readable format."""
    if not employees:
        print("\nNo matching employee records found.")
        return

    print("\n" + "-" * 75)
    print(
        f"{'ID':<10}{'Name':<15}"
        f"{'Department':<18}{'Salary':>12}"
    )
    print("-" * 75)

    for employee in employees:
        print(
            f"{employee['EmployeeID']:<10}"
            f"{employee['Name']:<15}"
            f"{employee['Department']:<18}"
            f"{employee['Salary']:>12,.2f}"
        )

        skills = employee.get("Skills", [])
        if isinstance(skills, list):
            print(f"    Skills: {', '.join(map(str, skills))}")

    print("-" * 75)


def search_employee(employees):
    """Search for an employee by name or ID."""
    search_term = input("Enter employee name or ID: ").strip()

    if not search_term:
        print("Search value cannot be empty.")
        return

    results = [
        employee for employee in employees
        if search_term.casefold() == str(employee["EmployeeID"]).casefold()
        or search_term.casefold() in employee["Name"].casefold()
    ]

    display_employees(results)


def filter_by_department(employees):
    """Filter employee records by department."""
    department = input("Enter department name: ").strip()

    if not department:
        print("Department cannot be empty.")
        return

    results = [
        employee for employee in employees
        if employee["Department"].casefold() == department.casefold()
    ]

    display_employees(results)


def filter_by_salary(employees):
    """Filter employees by a minimum salary."""
    try:
        minimum_salary = float(input("Enter minimum salary: "))

        if minimum_salary < 0:
            print("Salary cannot be negative.")
            return

        results = [
            employee for employee in employees
            if employee["Salary"] >= minimum_salary
        ]

        display_employees(results)

    except ValueError:
        print("Invalid input. Please enter a numeric salary.")


def show_summary(employees):
    """Display summary statistics for employee records."""
    if not employees:
        print("\nNo valid employee records available.")
        return

    total_salary = sum(employee["Salary"] for employee in employees)
    average_salary = total_salary / len(employees)

    highest_paid = max(employees, key=lambda employee: employee["Salary"])
    lowest_paid = min(employees, key=lambda employee: employee["Salary"])

    department_counts = {}

    for employee in employees:
        department = employee["Department"]
        department_counts[department] = (
            department_counts.get(department, 0) + 1
        )

    print("\n========== EMPLOYEE SUMMARY ==========")
    print(f"Total valid employees : {len(employees)}")
    print(f"Total salary          : {total_salary:,.2f}")
    print(f"Average salary        : {average_salary:,.2f}")
    print(
        f"Highest salary        : {highest_paid['Name']} "
        f"({highest_paid['Salary']:,.2f})"
    )
    print(
        f"Lowest salary         : {lowest_paid['Name']} "
        f"({lowest_paid['Salary']:,.2f})"
    )

    print("\nEmployees by department:")
    for department, count in sorted(department_counts.items()):
        print(f"{department}: {count}")

    print("======================================")


def main():
    """Run the JSON Data Processor menu."""
    employees = load_data()

    if not employees:
        print("No valid employee records loaded. Check data.json.")
        return

    while True:
        print("\n========== JSON DATA PROCESSOR ==========")
        print("1. Display all employees")
        print("2. Search employee by name or ID")
        print("3. Filter employees by department")
        print("4. Filter employees by minimum salary")
        print("5. Display employee summary")
        print("6. Exit")
        print("=========================================")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            display_employees(employees)
        elif choice == "2":
            search_employee(employees)
        elif choice == "3":
            filter_by_department(employees)
        elif choice == "4":
            filter_by_salary(employees)
        elif choice == "5":
            show_summary(employees)
        elif choice == "6":
            print("Thank you for using JSON Data Processor!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 6.")


if __name__ == "__main__":
    main()
