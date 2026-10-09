
import csv
from pathlib import Path
from datetime import datetime

# File paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "employees.csv"
OUTPUT_FILE = BASE_DIR / "summary_report.txt"


def read_csv_file(file_path):
    """Read employee records from a CSV file."""
    employees = []

    try:
        with file_path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            required_columns = {
                "EmployeeID", "Name", "Department", "Salary"
            }

            if not reader.fieldnames:
                raise ValueError("The CSV file is empty or has no header.")

            if not required_columns.issubset(set(reader.fieldnames)):
                raise ValueError(
                    "CSV must contain EmployeeID, Name, "
                    "Department, and Salary columns."
                )

            for row in reader:
                employees.append(row)

    except FileNotFoundError:
        print(f"Error: Input file not found: {file_path.name}")
        return None
    except (OSError, csv.Error, ValueError) as error:
        print(f"Error reading CSV file: {error}")
        return None

    return employees


def process_data(employees):
    """Calculate statistics and track invalid salary values."""
    valid_records = []
    salaries = []
    missing_salaries = 0
    invalid_salaries = 0

    department_counts = {}
    department_salary_totals = {}

    for employee in employees:
        name = (employee.get("Name") or "").strip()
        department = (employee.get("Department") or "").strip()
        salary_text = (employee.get("Salary") or "").strip()

        if not name or not department:
            invalid_salaries += 1
            continue

        if not salary_text:
            missing_salaries += 1
            continue

        try:
            salary = float(salary_text)

            if not (0 <= salary < float("inf")):
                raise ValueError("Salary must be a finite, non-negative number.")

        except ValueError:
            invalid_salaries += 1
            continue

        valid_records.append(employee)
        salaries.append(salary)

        department_counts[department] = (
            department_counts.get(department, 0) + 1
        )

        department_salary_totals[department] = (
            department_salary_totals.get(department, 0) + salary
        )

    total_salary = sum(salaries)
    average_salary = total_salary / len(salaries) if salaries else 0
    highest_salary = max(salaries) if salaries else 0
    lowest_salary = min(salaries) if salaries else 0

    # Find employees with the highest salary
    highest_paid = [
        employee["Name"].strip()
        for employee in valid_records
        if float(employee["Salary"].strip()) == highest_salary
    ]

    # Calculate average salary by department
    department_averages = {}

    for department, total in department_salary_totals.items():
        department_averages[department] = (
            total / department_counts[department]
        )

    return {
        "total_records": len(employees),
        "valid_records": len(valid_records),
        "missing_salaries": missing_salaries,
        "invalid_salaries": invalid_salaries,
        "total_salary": total_salary,
        "average_salary": average_salary,
        "highest_salary": highest_salary,
        "lowest_salary": lowest_salary,
        "highest_paid": highest_paid,
        "department_counts": department_counts,
        "department_averages": department_averages,
    }


def generate_report(stats):
    """Format the calculated statistics into a text report."""
    lines = [
        "=" * 50,
        "          CSV DATA PROCESSOR REPORT",
        "=" * 50,
        f"Generated on: {datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        "GENERAL STATISTICS",
        "-" * 50,
        f"Total CSV records: {stats['total_records']}",
        f"Valid salary records: {stats['valid_records']}",
        f"Missing salary records: {stats['missing_salaries']}",
        f"Invalid or skipped records: {stats['invalid_salaries']}",
        "",
        "SALARY STATISTICS",
        "-" * 50,
        f"Total salary: Rs. {stats['total_salary']:,.2f}",
        f"Average salary: Rs. {stats['average_salary']:,.2f}",
        f"Highest salary: Rs. {stats['highest_salary']:,.2f}",
        f"Lowest salary: Rs. {stats['lowest_salary']:,.2f}",
        f"Highest-paid employee(s): "
        f"{', '.join(stats['highest_paid']) or 'None'}",
        "",
        "DEPARTMENT SUMMARY",
        "-" * 50,
    ]

    if stats["department_counts"]:
        for department in sorted(stats["department_counts"]):
            count = stats["department_counts"][department]
            average = stats["department_averages"][department]

            lines.append(
                f"{department}: {count} valid employee(s), "
                f"average salary Rs. {average:,.2f}"
            )
    else:
        lines.append("No valid department salary data available.")

    lines.extend(["", "=" * 50, "End of Report", "=" * 50])

    return "\n".join(lines)


def save_report(report, file_path):
    """Save the report to a text file."""
    try:
        file_path.write_text(report + "\n", encoding="utf-8")
        print(f"\nReport saved successfully to: {file_path.name}")
    except OSError as error:
        print(f"Error saving report: {error}")


def main():
    print("=" * 50)
    print("           CSV DATA PROCESSOR")
    print("=" * 50)

    employees = read_csv_file(INPUT_FILE)

    if employees is None:
        return

    if not employees:
        print("The CSV file contains no employee records.")
        return

    stats = process_data(employees)
    report = generate_report(stats)

    print("\n" + report)
    save_report(report, OUTPUT_FILE)


if __name__ == "__main__":
    main()
