
import streamlit as st
import pandas as pd
from datetime import date

from expense_tracker import (
    initialize_file,
    load_expenses,
    add_expense,
    get_category_summary,
    get_total_spending,
    get_monthly_expenses
)

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

initialize_file()

st.title("Simple Expense Tracker")
st.caption("Record expenses, track spending, and manage your budget.")

expenses = load_expenses()

total = get_total_spending(expenses)
count = len(expenses)
categories = get_category_summary(expenses)

col1, col2, col3 = st.columns(3)
col1.metric("Total Spending", f"₹{total:,.2f}")
col2.metric("Total Expenses", count)
col3.metric("Categories", len(categories))

st.divider()

add_tab, records_tab, reports_tab = st.tabs([
    "➕ Add Expense",
    "📋 All Expenses",
    "📊 Reports"
])

with add_tab:
    st.subheader("Add a New Expense")

    with st.form("expense_form", clear_on_submit=True):
        expense_date = st.date_input(
            "Expense Date",
            value=date.today()
        )

        category = st.selectbox(
            "Category",
            [
                "Food", "Travel", "Shopping", "Bills",
                "Education", "Healthcare", "Entertainment",
                "Other"
            ]
        )

        custom_category = st.text_input(
            "Custom category (optional)",
            placeholder="Enter a category if not listed"
        )

        description = st.text_input(
            "Description",
            placeholder="e.g. Lunch, bus fare, electricity bill"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            max_value=1_000_000_000.00,
            value=100.00,
            step=10.00,
            format="%.2f"
        )

        submitted = st.form_submit_button(
            "Save Expense",
            use_container_width=True
        )

        if submitted:
            final_category = (
                custom_category.strip()
                if custom_category.strip()
                else category
            )

            try:
                add_expense(
                    expense_date,
                    final_category,
                    description,
                    amount
                )
                st.success("Expense saved successfully!")
                st.rerun()

            except (ValueError, OSError) as error:
                st.error(f"Could not save expense: {error}")

with records_tab:
    st.subheader("Expense Records")

    expenses = load_expenses()

    if expenses:
        df = pd.DataFrame(expenses)
        df = df.rename(columns={
            "date": "Date",
            "category": "Category",
            "description": "Description",
            "amount": "Amount (₹)"
        })

        st.dataframe(
            df.sort_values("Date", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Expenses as CSV",
            data=csv_data,
            file_name="expense_report.csv",
            mime="text/csv"
        )
    else:
        st.info("No expenses recorded yet. Add your first expense.")

with reports_tab:
    st.subheader("Spending Reports")

    expenses = load_expenses()
    categories = get_category_summary(expenses)

    if expenses:
        st.markdown("#### Category-wise Summary")

        category_df = pd.DataFrame(
            list(categories.items()),
            columns=["Category", "Total Spending (₹)"]
        )

        st.dataframe(
            category_df,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            category_df.set_index("Category")
        )

        st.markdown("#### Monthly Spending Report")

        selected_month = st.text_input(
            "Enter month (YYYY-MM)",
            value=date.today().strftime("%Y-%m")
        )

        if st.button("Generate Monthly Report"):
            try:
                monthly = get_monthly_expenses(
                    selected_month, expenses
                )

                st.metric(
                    "Monthly Total",
                    f"₹{get_total_spending(monthly):,.2f}"
                )

                if monthly:
                    st.dataframe(
                        pd.DataFrame(monthly),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No expenses found for this month.")

            except ValueError:
                st.error("Enter a valid month, such as 2026-10.")

        st.metric(
            "All-Time Total Spending",
            f"₹{get_total_spending(expenses):,.2f}"
        )

    else:
        st.info("Add some expenses to generate spending reports.")
