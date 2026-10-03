"""
Temperature Converter

A simple command-line application that converts temperatures
between Celsius, Fahrenheit, and Kelvin.
"""

from converter import (
    celsius_to_fahrenheit,
    celsius_to_kelvin,
    fahrenheit_to_celsius,
    fahrenheit_to_kelvin,
    kelvin_to_celsius,
    kelvin_to_fahrenheit,
    is_valid_temperature
)


def display_header():
    """Display the application header."""
    print("\n" + "=" * 50)
    print("           TEMPERATURE CONVERTER")
    print("=" * 50)


def display_units():
    """Display available temperature units."""
    print("\nAvailable Units:")
    print("1. Celsius (°C)")
    print("2. Fahrenheit (°F)")
    print("3. Kelvin (K)")


def get_unit():
    """Get and validate the temperature unit from the user."""

    while True:
        display_units()
        choice = input("\nSelect a unit (1-3): ").strip()

        if choice == "1":
            return "C"

        elif choice == "2":
            return "F"

        elif choice == "3":
            return "K"

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")


def get_temperature(unit):
    """Get and validate the temperature value."""

    while True:
        try:
            value = float(
                input(f"Enter temperature in {unit}: ").strip()
            )

            if not is_valid_temperature(value, unit):
                if unit == "C":
                    print(
                        "Invalid temperature. "
                        "Celsius cannot be below -273.15 °C."
                    )

                elif unit == "F":
                    print(
                        "Invalid temperature. "
                        "Fahrenheit cannot be below -459.67 °F."
                    )

                elif unit == "K":
                    print(
                        "Invalid temperature. "
                        "Kelvin cannot be below 0 K."
                    )

                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def convert_temperature(value, from_unit, to_unit):
    """Convert a temperature from one unit to another."""

    if from_unit == to_unit:
        return value

    if from_unit == "C" and to_unit == "F":
        return celsius_to_fahrenheit(value)

    elif from_unit == "C" and to_unit == "K":
        return celsius_to_kelvin(value)

    elif from_unit == "F" and to_unit == "C":
        return fahrenheit_to_celsius(value)

    elif from_unit == "F" and to_unit == "K":
        return fahrenheit_to_kelvin(value)

    elif from_unit == "K" and to_unit == "C":
        return kelvin_to_celsius(value)

    elif from_unit == "K" and to_unit == "F":
        return kelvin_to_fahrenheit(value)

    return None


def get_unit_name(unit):
    """Return the full name of a temperature unit."""

    names = {
        "C": "Celsius",
        "F": "Fahrenheit",
        "K": "Kelvin"
    }

    return names[unit]


def get_unit_symbol(unit):
    """Return the symbol of a temperature unit."""

    symbols = {
        "C": "°C",
        "F": "°F",
        "K": "K"
    }

    return symbols[unit]


def main():
    """Run the Temperature Converter application."""

    while True:
        display_header()

        print("\n1. Convert Temperature")
        print("2. Exit")

        choice = input("\nEnter your choice (1-2): ").strip()

        if choice == "1":

            # Get source unit
            from_unit = get_unit()

            # Get temperature
            temperature = get_temperature(from_unit)

            # Get target unit
            print("\nSelect the unit to convert to:")

            if from_unit == "C":
                print("1. Fahrenheit (°F)")
                print("2. Kelvin (K)")

                target_choice = input("\nEnter choice (1-2): ").strip()

                if target_choice == "1":
                    to_unit = "F"
                elif target_choice == "2":
                    to_unit = "K"
                else:
                    print("\nInvalid target unit.")
                    continue

            elif from_unit == "F":
                print("1. Celsius (°C)")
                print("2. Kelvin (K)")

                target_choice = input("\nEnter choice (1-2): ").strip()

                if target_choice == "1":
                    to_unit = "C"
                elif target_choice == "2":
                    to_unit = "K"
                else:
                    print("\nInvalid target unit.")
                    continue

            else:
                print("1. Celsius (°C)")
                print("2. Fahrenheit (°F)")

                target_choice = input("\nEnter choice (1-2): ").strip()

                if target_choice == "1":
                    to_unit = "C"
                elif target_choice == "2":
                    to_unit = "F"
                else:
                    print("\nInvalid target unit.")
                    continue

            # Perform conversion
            result = convert_temperature(
                temperature,
                from_unit,
                to_unit
            )

            # Display result
            print("\n" + "-" * 50)
            print("CONVERSION RESULT")
            print("-" * 50)

            print(
                f"{temperature:.2f} {get_unit_symbol(from_unit)} "
                f"= {result:.2f} {get_unit_symbol(to_unit)}"
            )

            print(
                f"({get_unit_name(from_unit)} → "
                f"{get_unit_name(to_unit)})"
            )

            print("-" * 50)

        elif choice == "2":
            print("\nThank you for using Temperature Converter!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1 or 2.")


if __name__ == "__main__":
    main()