
from bank_account import BankAccount


def get_amount(prompt):
    """Accept and validate a transaction amount."""
    try:
        amount = float(input(prompt))

        if amount <= 0:
            print("Error: Amount must be greater than zero.")
            return None

        return amount

    except ValueError:
        print("Error: Please enter a valid number.")
        return None


def run_terminal():
    """Run the menu-driven banking application."""

    account = BankAccount()

    while True:
        print("\n" + "=" * 40)
        print("       BANK ACCOUNT SIMULATOR")
        print("=" * 40)
        print("1. Balance Inquiry")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transaction History")
        print("5. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            print(f"\nAvailable Balance: ₹{account.get_balance():,.2f}")

        elif choice == "2":
            amount = get_amount("Enter deposit amount: ₹")

            if amount is not None:
                success, message = account.deposit(amount)
                print(message)

                if success:
                    print(
                        f"Updated Balance: "
                        f"₹{account.get_balance():,.2f}"
                    )

        elif choice == "3":
            amount = get_amount("Enter withdrawal amount: ₹")

            if amount is not None:
                success, message = account.withdraw(amount)
                print(message)

                if success:
                    print(
                        f"Remaining Balance: "
                        f"₹{account.get_balance():,.2f}"
                    )

        elif choice == "4":
            transactions = account.get_transactions()

            print("\nTRANSACTION HISTORY")
            print("-" * 40)

            if not transactions:
                print("No transactions available.")

            else:
                for index, transaction in enumerate(
                    transactions, start=1
                ):
                    transaction_type = transaction["type"]
                    amount = transaction["amount"]
                    balance = transaction["balance"]

                    sign = "+" if transaction_type == "Deposit" else "-"

                    print(f"\nTransaction #{index}")
                    print(f"Type: {transaction_type}")
                    print(f"Amount: {sign}₹{amount:,.2f}")
                    print(f"Balance after transaction: ₹{balance:,.2f}")

        elif choice == "5":
            print("\nThank you for using Bank Account Simulator!")
            break

        else:
            print("Invalid choice. Please select an option from 1 to 5.")


if __name__ == "__main__":
    run_terminal()