"""
Temperature Conversion Functions

This module contains functions for converting temperatures
between Celsius, Fahrenheit, and Kelvin.
"""


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin."""
    return (fahrenheit - 32) * 5 / 9 + 273.15


def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit."""
    return (kelvin - 273.15) * 9 / 5 + 32


def is_valid_temperature(value, unit):
    """
    Check whether a temperature is physically meaningful.

    Kelvin cannot be below 0 K.
    Celsius cannot be below -273.15 °C.
    Fahrenheit cannot be below -459.67 °F.
    """

    if unit == "C":
        return value >= -273.15

    elif unit == "F":
        return value >= -459.67

    elif unit == "K":
        return value >= 0

    return False