# Shopping Bill Generator

## Overview

The Shopping Bill Generator is a Python-based mini-project that creates a
formatted shopping bill from product names, quantities, and prices.

The project demonstrates practical usage of Python lists, dictionaries,
loops, functions, input validation, and arithmetic calculations.

## Objective

The objective of this project is to develop a simple shopping bill system
that calculates:

- Item-wise totals
- Subtotal
- Discount
- Tax
- Final payable amount

## Features

- Accept product names from the user
- Accept product quantities
- Accept product prices
- Calculate individual item totals
- Store product information using dictionaries
- Store multiple products using a list
- Calculate subtotal
- Apply a 10% discount for bills of ₹1000 or more
- Calculate 5% tax
- Generate a formatted itemized bill
- Validate invalid quantities
- Validate invalid prices
- Handle invalid user input
- Use reusable functions for calculations

## Technologies Used

- Python
- Lists
- Dictionaries
- Loops
- Functions
- Conditional statements
- Exception handling
- Arithmetic operations

## Discount and Tax Rules

### Discount

If the subtotal is ₹1000 or more:

```text
Discount = 10%