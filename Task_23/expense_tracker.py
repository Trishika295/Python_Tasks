
import csv
import math
from pathlib import Path
from datetime import date, datetime
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = BASE_DIR / "expenses.csv"

FIELDNAMES = ["date", "category", "description", "amount"]


def initialize_file():
    """Create the CSV file with column headers if necessary."""
    if not FILE_NAME.exists() or FILE_NAME.stat().st_size == 0:
        with FILE_NAME.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_expenses():
    """Load valid expense records from CSV."""
    initialize_file()
    expenses = []

    with FILE_NAME.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not set(FIELDNAMES).issubset(
            reader.fieldnames
        ):
            raise ValueError("The CSV file has an invalid header.")

        for row in reader:
            try:
                expense_date = date.fromisoformat(row["date"])
                category = row["category"].strip()
                description = row["description"].strip()
                amount = float(row["amount"])

                if (
                    category
                    and description
                    and math.isfinite(amount)
                    and amount > 0
                ):
                    expenses.append({
                        "date": expense_date.isoformat(),
                        "category": category,
                        "description": description,
                        "amount": round(amount, 2)
                    })
            except (ValueError, TypeError, KeyError):
                continue

    return expenses


def add_expense(expense_date, category, description, amount):
    """Validate and save a new expense."""
    if isinstance(expense_date, datetime):
        expense_date = expense_date.date()

    if isinstance(expense_date, date):
        expense_date = expense_date.isoformat()

    try:
        parsed_date = date.fromisoformat(str(expense_date))
    except (ValueError, TypeError):
        raise ValueError("Enter a valid date in YYYY-MM-DD format.")

    category = str(category).strip()
    description = str(description).strip()

    if not category:
        raise ValueError("Category cannot be empty.")

    if not description:
        raise ValueError("Description cannot be empty.")

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")

    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    expense = {
        "date": parsed_date.isoformat(),
        "category": category,
        "description": description,
        "amount": round(amount, 2)
    }

    initialize_file()

    with FILE_NAME.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(expense)

    return expense


def get_category_summary(expenses=None):
    """Return total spending grouped by category."""
    if expenses is None:
        expenses = load_expenses()

    totals = defaultdict(float)

    for expense in expenses:
        totals[expense["category"]] += expense["amount"]

    return {
        category: round(total, 2)
        for category, total in sorted(totals.items())
    }


def get_total_spending(expenses=None):
    """Calculate total expenditure."""
    if expenses is None:
        expenses = load_expenses()

    return round(sum(item["amount"] for item in expenses), 2)


def get_monthly_expenses(month, expenses=None):
    """Return expenses for a YYYY-MM month."""
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise ValueError("Month must use YYYY-MM format.")

    if expenses is None:
        expenses = load_expenses()

    return [
        expense for expense in expenses
        if expense["date"].startswith(month)
    ]


def run_terminal():
    """Run the command-line expense tracker."""
    initialize_file()

    while True:
        print("\n" + "=" * 42)
        print("       SIMPLE EXPENSE TRACKER")
        print("=" * 42)
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category-wise Summary")
        print("4. Total Spending Report")
        print("5. Monthly Spending Summary")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        try:
            if choice == "1":
                expense_date = input(
                    "Date (YYYY-MM-DD, blank for today): "
                ).strip() or date.today().isoformat()

                category = input("Category: ")
                description = input("Description: ")
                amount = input("Amount (Rs.): ")

                add_expense(
                    expense_date, category, description, amount
                )
                print("Expense saved successfully!")

            elif choice == "2":
                expenses = load_expenses()

                if not expenses:
                    print("No expenses recorded.")
                else:
                    for item in expenses:
                        print(
                            f"{item['date']} | {item['category']} | "
                            f"{item['description']} | "
                            f"Rs. {item['amount']:.2f}"
                        )

            elif choice == "3":
                for category, total in get_category_summary().items():
                    print(f"{category}: Rs. {total:.2f}")

            elif choice == "4":
                expenses = load_expenses()
                print(f"Number of expenses: {len(expenses)}")
                print(f"Total spending: Rs. {get_total_spending(expenses):.2f}")

            elif choice == "5":
                month = input("Enter month (YYYY-MM): ").strip()
                expenses = get_monthly_expenses(month)
                print(f"\nReport for {month}")

                for item in expenses:
                    print(
                        f"{item['date']} | {item['category']} | "
                        f"{item['description']} | Rs. {item['amount']:.2f}"
                    )

                print(
                    f"Monthly total: Rs. {get_total_spending(expenses):.2f}"
                )

            elif choice == "6":
                print("Thank you for using Expense Tracker!")
                break

            else:
                print("Invalid choice. Select a number from 1 to 6.")

        except ValueError as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"File error: {error}")


if __name__ == "__main__":
    run_terminal()
