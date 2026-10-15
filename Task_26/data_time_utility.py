
from datetime import date, datetime, time, timedelta


DATE_FORMAT = "%Y-%m-%d"


def get_valid_date(prompt):
    """Read and validate a date in YYYY-MM-DD format."""
    while True:
        user_input = input(prompt).strip()

        try:
            return datetime.strptime(user_input, DATE_FORMAT).date()
        except ValueError:
            print("Invalid date! Please use YYYY-MM-DD (example: 2004-08-25).")


def calculate_age():
    """Calculate age in completed years."""
    print("\n--- AGE CALCULATOR ---")
    dob = get_valid_date("Enter your date of birth (YYYY-MM-DD): ")
    today = date.today()

    if dob > today:
        print("Error: Date of birth cannot be in the future.")
        return

    age = today.year - dob.year
    birthday_not_reached = (today.month, today.day) < (dob.month, dob.day)

    if birthday_not_reached:
        age -= 1

    print(f"Date of birth: {dob.strftime('%d-%B-%Y')}")
    print(f"Current date: {today.strftime('%d-%B-%Y')}")
    print(f"Your age is: {age} years")


def calculate_days_between():
    """Calculate the elapsed number of days between two dates."""
    print("\n--- DAYS BETWEEN DATES ---")
    start_date = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    end_date = get_valid_date("Enter the end date (YYYY-MM-DD): ")

    days = abs((end_date - start_date).days)

    print(f"Start date: {start_date}")
    print(f"End date:   {end_date}")
    print(f"Difference: {days} days")


def calculate_working_days():
    """Count weekdays between two dates, including both endpoints."""
    print("\n--- WORKING DAYS CALCULATOR ---")
    start_date = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    end_date = get_valid_date("Enter the end date (YYYY-MM-DD): ")

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    working_days = 0
    current_date = start_date

    while current_date <= end_date:
        # Monday = 0, Tuesday = 1, ..., Sunday = 6
        if current_date.weekday() < 5:
            working_days += 1

        current_date += timedelta(days=1)

    print(f"Start date: {start_date}")
    print(f"End date:   {end_date}")
    print(f"Working days (Monday-Friday): {working_days}")
    print("Note: Public holidays are not excluded.")


def format_date_time():
    """Display a date in different formats."""
    print("\n--- DATE FORMATTER ---")
    entered_date = get_valid_date("Enter a date (YYYY-MM-DD): ")

    formats = {
        "1": ("%d-%m-%Y", "DD-MM-YYYY"),
        "2": ("%m/%d/%Y", "MM/DD/YYYY"),
        "3": ("%d %B %Y", "Day Month Year"),
        "4": ("%A, %d %B %Y", "Full date with weekday"),
        "5": ("%Y-%m-%d", "ISO format"),
    }

    print("\nChoose a format:")
    for key, (_, description) in formats.items():
        print(f"{key}. {description}")

    choice = input("Enter your choice (1-5): ").strip()

    if choice in formats:
        format_string, description = formats[choice]
        print(f"{description}: {entered_date.strftime(format_string)}")
    else:
        print("Invalid format choice.")


def show_current_date_time():
    """Display the current system date and time."""
    print("\n--- CURRENT DATE AND TIME ---")
    now = datetime.now()

    print("Current date:      ", now.strftime("%d-%m-%Y"))
    print("Current time:      ", now.strftime("%I:%M:%S %p"))
    print("Date and time:     ", now.strftime("%A, %d %B %Y %H:%M:%S"))
    print("ISO date and time: ", now.isoformat(timespec="seconds"))


def show_sample_calculations():
    """Display examples of date and time operations."""
    print("\n--- SAMPLE CALCULATIONS ---")

    first_date = date(2024, 1, 1)
    second_date = date(2024, 1, 10)

    print(f"1. Days between {first_date} and {second_date}: "
          f"{(second_date - first_date).days} days")

    leap_year_date = date(2024, 2, 29)
    print(f"2. Leap-year date: {leap_year_date.strftime('%d %B %Y')}")

    example_start = date(2024, 1, 1)
    example_end = date(2024, 1, 7)
    working_days = sum(
        1
        for day_offset in range((example_end - example_start).days + 1)
        if (example_start + timedelta(days=day_offset)).weekday() < 5
    )

    print(f"3. Working days from {example_start} to {example_end}: "
          f"{working_days}")

    example_datetime = datetime(2024, 6, 15, 14, 30, 0)
    print("4. Formatted date and time:",
          example_datetime.strftime("%d-%m-%Y %I:%M %p"))


def main():
    """Display the menu and run the selected operation."""
    while True:
        print("\n" + "=" * 42)
        print("       PYTHON DATE AND TIME UTILITY")
        print("=" * 42)
        print("1. Calculate age")
        print("2. Calculate days between dates")
        print("3. Calculate working days")
        print("4. Format a date")
        print("5. Show current date and time")
        print("6. View sample calculations")
        print("0. Exit")
        print("=" * 42)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            calculate_age()
        elif choice == "2":
            calculate_days_between()
        elif choice == "3":
            calculate_working_days()
        elif choice == "4":
            format_date_time()
        elif choice == "5":
            show_current_date_time()
        elif choice == "6":
            show_sample_calculations()
        elif choice == "0":
            print("Thank you for using the Date and Time Utility!")
            break
        else:
            print("Invalid choice! Please select an option from 0 to 6.")


if __name__ == "__main__":
    main()
