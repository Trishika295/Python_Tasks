
"""
Python Utility Module
Reusable functions for validation, formatting, calculations,
and file handling.
"""

import re
from pathlib import Path


# =========================================================
# 1. VALIDATION UTILITIES
# =========================================================

def is_valid_email(email: str) -> bool:
    """Return True if the email has a basic valid format."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email.strip()))


def is_valid_phone(phone: str) -> bool:
    """Return True if the phone number contains exactly 10 digits."""
    return phone.isdigit() and len(phone) == 10


def is_number(value: str) -> bool:
    """Return True if the supplied text represents a finite number."""
    try:
        number = float(value)
        return number == number and abs(number) != float("inf")
    except (ValueError, TypeError):
        return False


# =========================================================
# 2. FORMATTING UTILITIES
# =========================================================

def format_name(name: str) -> str:
    """Remove extra spaces and capitalize each part of a name."""
    return " ".join(name.strip().split()).title()


def format_currency(amount: float) -> str:
    """Format a number as Indian Rupees."""
    return f"₹{amount:,.2f}"


def format_text(text: str) -> str:
    """Remove extra spaces and normalize text to lowercase."""
    return " ".join(text.strip().split()).lower()


# =========================================================
# 3. CALCULATION UTILITIES
# =========================================================

def calculate_percentage(value: float, total: float) -> float:
    """Calculate value as a percentage of total."""
    if total == 0:
        raise ValueError("Total cannot be zero.")

    return (value / total) * 100


def calculate_average(numbers: list[float]) -> float:
    """Return the average of a non-empty list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate the average of an empty list.")

    return sum(numbers) / len(numbers)


def calculate_total(numbers: list[float]) -> float:
    """Return the sum of the supplied numbers."""
    return sum(numbers)


# =========================================================
# 4. FILE UTILITIES
# =========================================================

def file_exists(file_path: str) -> bool:
    """Check whether a file exists at the specified path."""
    return Path(file_path).is_file()


def read_text_file(file_path: str) -> str:
    """Read and return the contents of a UTF-8 text file."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    return path.read_text(encoding="utf-8")


def write_text_file(file_path: str, content: str) -> None:
    """Write text to a UTF-8 file, creating parent folders if needed."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# This module can be imported without running a demo automatically.
