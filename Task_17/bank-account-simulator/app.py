import streamlit as st

from bank_account import BankAccount


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bank Account Simulator",
    page_icon="🏦",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f1ea;
    }

    .main-header {
        background-color: #29251f;
        padding: 28px 35px;
        border-radius: 15px;
        margin-bottom: 25px;
    }

    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 32px;
    }

    .main-header p {
        color: #d8d0c5;
        margin-top: 8px;
        margin-bottom: 0;
    }

    .balance-card {
        background-color: #b56b45;
        padding: 28px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
    }

    .balance-title {
        font-size: 15px;
        margin-bottom: 8px;
    }

    .balance-value {
        font-size: 38px;
        font-weight: bold;
    }

    .section-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e2dbd2;
        margin-top: 20px;
    }

    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2dbd2;
        text-align: center;
    }

    .feature-number {
        color: #b56b45;
        font-size: 25px;
        font-weight: bold;
    }

    .transaction-card {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e2dbd2;
        margin-bottom: 12px;
    }

    .transaction-deposit {
        color: #34734a;
        font-weight: bold;
    }

    .transaction-withdrawal {
        color: #a54338;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "account" not in st.session_state:
    st.session_state.account = BankAccount()

account = st.session_state.account


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-header">
        <h1>🏦 Bank Account Simulator</h1>
        <p>
            Menu-driven banking application using Python and Streamlit
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CURRENT BALANCE
# ============================================================

st.markdown(
    f"""
    <div class="balance-card">
        <div class="balance-title">AVAILABLE BALANCE</div>
        <div class="balance-value">
            ₹{account.get_balance():,.2f}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR MENU
# ============================================================

st.sidebar.title("🏦 Banking Menu")

st.sidebar.markdown(
    "Select an operation:"
)

menu = st.sidebar.radio(
    "",
    [
        "Home",
        "Balance Inquiry",
        "Deposit",
        "Withdraw",
        "Transaction History"
    ]
)


# ============================================================
# HOME
# ============================================================

if menu == "Home":

    st.header("Welcome to Bank Account Simulator")

    st.write(
        "Use the banking menu on the left to perform "
        "different account operations."
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">01</div>
                <h4>Balance</h4>
                <p>Check your current account balance.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">02</div>
                <h4>Deposit</h4>
                <p>Add money to your account.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">03</div>
                <h4>Withdraw</h4>
                <p>Withdraw money from your account.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">04</div>
                <h4>History</h4>
                <p>View your transaction history.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# BALANCE INQUIRY
# ============================================================

elif menu == "Balance Inquiry":

    st.header("Balance Inquiry")

    current_balance = account.get_balance()

    st.success(
        f"Your current balance is ₹{current_balance:,.2f}"
    )

    st.write(
        "This section displays the current available balance "
        "of your bank account."
    )


# ============================================================
# DEPOSIT
# ============================================================

elif menu == "Deposit":

    st.header("Deposit Money")

    st.write(
        "Enter the amount you want to deposit into your account."
    )

    amount = st.number_input(
        "Deposit Amount (₹)",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )

    if st.button(
        "Deposit Money",
        type="primary",
        use_container_width=True
    ):

        success, message = account.deposit(amount)

        if success:

            st.success(message)

            st.info(
                f"Updated balance: "
                f"₹{account.get_balance():,.2f}"
            )

        else:

            st.error(message)


# ============================================================
# WITHDRAW
# ============================================================

elif menu == "Withdraw":

    st.header("Withdraw Money")

    st.write(
        "Enter the amount you want to withdraw."
    )

    st.info(
        f"Available balance: "
        f"₹{account.get_balance():,.2f}"
    )

    amount = st.number_input(
        "Withdrawal Amount (₹)",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )

    if st.button(
        "Withdraw Money",
        type="primary",
        use_container_width=True
    ):

        success, message = account.withdraw(amount)

        if success:

            st.success(message)

            st.info(
                f"Remaining balance: "
                f"₹{account.get_balance():,.2f}"
            )

        else:

            st.error(message)


# ============================================================
# TRANSACTION HISTORY
# ============================================================

elif menu == "Transaction History":

    st.header("Transaction History")

    transactions = account.get_transactions()

    if len(transactions) == 0:

        st.info(
            "No transactions available yet."
        )

    else:

        st.write(
            f"Total transactions: {len(transactions)}"
        )

        # Loop through transaction history
        for index, transaction in enumerate(
            transactions,
            start=1
        ):

            transaction_type = transaction["type"]
            amount = transaction["amount"]
            balance = transaction["balance"]

            if transaction_type == "Deposit":

                st.markdown(
                    f"""
                    <div class="transaction-card">
                        <strong>
                            Transaction #{index} — Deposit
                        </strong>

                        <p class="transaction-deposit">
                            + ₹{amount:,.2f}
                        </p>

                        <p>
                            Balance after transaction:
                            ₹{balance:,.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="transaction-card">
                        <strong>
                            Transaction #{index} — Withdrawal
                        </strong>

                        <p class="transaction-withdrawal">
                            - ₹{amount:,.2f}
                        </p>

                        <p>
                            Balance after transaction:
                            ₹{balance:,.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Bank Account Simulator | Python + Streamlit"
)