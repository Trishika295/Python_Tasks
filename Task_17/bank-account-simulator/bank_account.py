class BankAccount:
    """Simple bank account simulator."""

    def __init__(self):
        self.balance = 0.0
        self.transactions = []

    def get_balance(self):
        """Return the current account balance."""
        return self.balance

    def deposit(self, amount):
        """Deposit money into the account."""

        if amount <= 0:
            return False, "Deposit amount must be greater than zero."

        self.balance += amount

        self.transactions.append({
            "type": "Deposit",
            "amount": amount,
            "balance": self.balance
        })

        return True, f"₹{amount:.2f} deposited successfully."

    def withdraw(self, amount):
        """Withdraw money from the account."""

        if amount <= 0:
            return False, "Withdrawal amount must be greater than zero."

        if amount > self.balance:
            return False, "Withdrawal rejected: insufficient balance."

        self.balance -= amount

        self.transactions.append({
            "type": "Withdrawal",
            "amount": amount,
            "balance": self.balance
        })

        return True, f"₹{amount:.2f} withdrawn successfully."

    def get_transactions(self):
        """Return transaction history."""
        return self.transactions