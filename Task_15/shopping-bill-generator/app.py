
# Discount and tax configuration
DISCOUNT_THRESHOLD = 1000
DISCOUNT_RATE = 10
TAX_RATE = 5


def calculate_item_total(quantity, price):
    """
    Calculate the total price for a single product.
    """
    return quantity * price


def calculate_subtotal(products):
    """
    Calculate the subtotal of all products.
    """
    subtotal = 0

    for product in products:
        subtotal += product["total"]

    return subtotal


def calculate_discount(subtotal):
    """
    Calculate discount based on the subtotal.
    10% discount is given when subtotal is
    greater than or equal to ₹1000.
    """
    if subtotal >= DISCOUNT_THRESHOLD:
        return subtotal * DISCOUNT_RATE / 100

    return 0


def calculate_tax(amount):
    """
    Calculate tax on the amount after discount.
    """
    return amount * TAX_RATE / 100


def display_bill(products, subtotal, discount, tax, final_amount):
    """
    Display the formatted shopping bill.
    """

    print("\n")
    print("=" * 70)
    print("                    SHOPPING BILL")
    print("=" * 70)

    print(
        f"{'Product':<25}"
        f"{'Qty':>8}"
        f"{'Unit Price':>15}"
        f"{'Total':>15}"
    )

    print("-" * 70)

    for product in products:
        print(
            f"{product['name']:<25}"
            f"{product['quantity']:>8}"
            f"₹{product['price']:>13.2f}"
            f"₹{product['total']:>13.2f}"
        )

    print("-" * 70)

    print(f"{'Subtotal':<50} ₹{subtotal:>12.2f}")
    print(f"{'Discount':<50} ₹{discount:>12.2f}")
    print(f"{'Tax (' + str(TAX_RATE) + '%)':<50} ₹{tax:>12.2f}")

    print("-" * 70)

    print(f"{'FINAL AMOUNT':<50} ₹{final_amount:>12.2f}")

    print("=" * 70)
    print("             Thank you for shopping!")
    print("=" * 70)


def get_positive_integer(message):
    """
    Get a valid positive integer from the user.
    """

    while True:
        try:
            value = int(input(message))

            if value <= 0:
                print("Please enter a quantity greater than 0.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_positive_float(message):
    """
    Get a valid positive price from the user.
    """

    while True:
        try:
            value = float(input(message))

            if value <= 0:
                print("Please enter a price greater than 0.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a valid price.")


def add_products():
    """
    Accept product information from the user.
    """

    products = []

    print("\n" + "=" * 50)
    print("         ENTER SHOPPING DETAILS")
    print("=" * 50)

    while True:

        # Product name
        while True:
            name = input("\nEnter product name: ").strip()

            if name:
                break

            print("Product name cannot be empty.")

        # Quantity
        quantity = get_positive_integer(
            "Enter quantity: "
        )

        # Price
        price = get_positive_float(
            "Enter price per item: ₹"
        )

        # Calculate item total
        total = calculate_item_total(quantity, price)

        # Store product as a dictionary
        product = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "total": total
        }

        products.append(product)

        print(
            f"\n{quantity} × {name} "
            f"added successfully. "
            f"Item total: ₹{total:.2f}"
        )

        # Ask whether the user wants another product
        while True:
            choice = input(
                "\nDo you want to add another product? (y/n): "
            ).strip().lower()

            if choice in ["y", "n"]:
                break

            print("Please enter y or n.")

        if choice == "n":
            break

    return products


def main():
    """
    Main function of the Shopping Bill Generator.
    """

    print("\n" + "=" * 60)
    print("             SHOPPING BILL GENERATOR")
    print("=" * 60)

    print("\nDiscount Policy:")
    print(
        f"Orders of ₹{DISCOUNT_THRESHOLD} or more "
        f"receive a {DISCOUNT_RATE}% discount."
    )

    print(f"Tax Rate: {TAX_RATE}%")

    # Get products
    products = add_products()

    # Calculate subtotal
    subtotal = calculate_subtotal(products)

    # Calculate discount
    discount = calculate_discount(subtotal)

    # Amount after discount
    amount_after_discount = subtotal - discount

    # Calculate tax
    tax = calculate_tax(amount_after_discount)

    # Calculate final amount
    final_amount = amount_after_discount + tax

    # Display bill
    display_bill(
        products,
        subtotal,
        discount,
        tax,
        final_amount
    )


# Program execution
if __name__ == "__main__":
    main()