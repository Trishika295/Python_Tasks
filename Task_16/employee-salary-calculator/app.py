# app.py

from employee_data import employees
from salary_calculator import calculate_salary


def get_positive_number(prompt):
    """
    Get a positive numeric value from the user.
    """

    while True:
        try:
            value = float(input(prompt))

            if value <= 0:
                print("Please enter a value greater than 0.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_employee_id():
    """
    Get a valid employee ID.
    """

    while True:
        employee_id = input("Enter Employee ID: ").strip()

        if employee_id == "":
            print("Employee ID cannot be empty.")
        else:
            return employee_id


def get_employee_name():
    """
    Get a valid employee name.
    """

    while True:
        name = input("Enter Employee Name: ").strip()

        if name == "":
            print("Employee name cannot be empty.")
        else:
            return name


def get_department():
    """
    Get employee department.
    """

    while True:
        department = input("Enter Department: ").strip()

        if department == "":
            print("Department cannot be empty.")
        else:
            return department


def display_salary_slip(salary):
    """
    Display complete salary calculation.
    """

    print("\n")
    print("=" * 60)
    print("                 EMPLOYEE SALARY SLIP")
    print("=" * 60)

    print(f"Employee ID       : {salary['employee_id']}")
    print(f"Employee Name     : {salary['name']}")
    print(f"Department        : {salary['department']}")

    print("-" * 60)
    print("EARNINGS")
    print("-" * 60)

    print(f"Basic Salary      : ₹{salary['basic_salary']:,.2f}")
    print(f"HRA               : ₹{salary['hra']:,.2f}")
    print(f"DA                : ₹{salary['da']:,.2f}")
    print(
        f"Special Allowance : ₹{salary['special_allowance']:,.2f}"
    )

    print("-" * 60)
    print(
        f"Total Allowances  : ₹{salary['total_allowances']:,.2f}"
    )
    print(
        f"Gross Salary      : ₹{salary['gross_salary']:,.2f}"
    )

    print("\n")
    print("-" * 60)
    print("DEDUCTIONS")
    print("-" * 60)

    print(f"PF                : ₹{salary['pf']:,.2f}")
    print(
        f"Professional Tax  : ₹{salary['professional_tax']:,.2f}"
    )
    print(
        f"Income Tax        : ₹{salary['income_tax']:,.2f}"
    )

    print("-" * 60)
    print(
        f"Total Deductions  : ₹{salary['total_deductions']:,.2f}"
    )

    print("=" * 60)
    print(
        f"NET SALARY        : ₹{salary['net_salary']:,.2f}"
    )
    print("=" * 60)


def calculate_new_salary():
    """
    Accept employee details and calculate salary.
    """

    print("\n")
    print("-" * 60)
    print("ENTER EMPLOYEE DETAILS")
    print("-" * 60)

    employee_id = get_employee_id()
    name = get_employee_name()
    department = get_department()

    basic_salary = get_positive_number(
        "Enter Basic Salary: ₹"
    )

    employee = {
        "employee_id": employee_id,
        "name": name,
        "department": department,
        "basic_salary": basic_salary
    }

    employees.append(employee)

    salary = calculate_salary(employee)

    display_salary_slip(salary)


def display_sample_employees():
    """
    Display all stored employee records.
    """

    print("\n")
    print("=" * 70)
    print("                    EMPLOYEE RECORDS")
    print("=" * 70)

    if not employees:
        print("No employee records available.")
        return

    for employee in employees:

        print(f"Employee ID : {employee['employee_id']}")
        print(f"Name        : {employee['name']}")
        print(f"Department  : {employee['department']}")
        print(f"Basic Salary: ₹{employee['basic_salary']:,.2f}")

        print("-" * 70)


def calculate_sample_salary():
    """
    Calculate and display salary for all sample employees.
    """

    print("\n")
    print("=" * 70)
    print("                 SAMPLE SALARY CALCULATIONS")
    print("=" * 70)

    for employee in employees:

        salary = calculate_salary(employee)

        print(f"\nEmployee: {salary['name']}")
        print(f"Employee ID: {salary['employee_id']}")
        print(f"Gross Salary: ₹{salary['gross_salary']:,.2f}")
        print(f"Total Deductions: ₹{salary['total_deductions']:,.2f}")
        print(f"Net Salary: ₹{salary['net_salary']:,.2f}")

        print("-" * 70)


def display_menu():
    """
    Display the application menu.
    """

    print("\n")
    print("=" * 60)
    print("             EMPLOYEE SALARY CALCULATOR")
    print("=" * 60)

    print("1. Calculate Salary for New Employee")
    print("2. View Employee Records")
    print("3. Calculate Sample Employee Salaries")
    print("4. Exit")

    print("=" * 60)


def main():
    """
    Main application function.
    """

    while True:

        display_menu()

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            calculate_new_salary()

        elif choice == "2":
            display_sample_employees()

        elif choice == "3":
            calculate_sample_salary()

        elif choice == "4":
            print("\nThank you for using Employee Salary Calculator!")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()