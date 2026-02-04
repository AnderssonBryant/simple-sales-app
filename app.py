import streamlit as st
import pandas as pd
from datetime import date,timedelta
from backend.menu import load_menu
from backend.sales import create_bulk_daily_sales, save_bulk_daily_sales, get_sales_history, get_detailed_sales
from backend.expenses import add_expense, get_expense_history
from backend.cash import  get_cash_balance
from backend.pdf_export import generate_detailed_sales_pdf, generate_sales_summary_pdf
from backend.reports import get_sales_report,get_cashflow_report,get_expense_report, get_sales_report_with_total
import os

st.set_page_config(
    page_title="Coffee POS",
    page_icon="☕",
    layout="wide"
)

st.title("Coffee Sales & Cashflow")

tab1, tab2, tab3, tab4 = st.tabs(["Sales", "Expenses","Reports","Charts"])

# ---------------- SALES ----------------
with tab1:
    menu = load_menu()

    st.header("Daily Sales Input")

    sale_date = st.date_input("Sale Date", value=date.today())

    qty_by_product = {}

    cols = st.columns(3)
    for i, row in menu.iterrows():
        col = cols[i % 3]
        qty = col.number_input(
            f"{row['product_name']} ({row['product_code']})",
            min_value=0,
            step=1,
            key=row["product_code"]
        )
        qty_by_product[row["product_code"]] = qty

    if st.button("Save Daily Sales"):
        sales = create_bulk_daily_sales(qty_by_product, sale_date)
        save_bulk_daily_sales(sales)
        st.success("Daily sales saved (auto-updated if existed)")

    st.divider()
    st.header("Sales History")

    history_df = get_sales_history()

    if history_df.empty:
        st.info("No sales recorded yet")
    else:
        menu = load_menu()

        history_df = history_df.merge(
            menu[["product_code", "product_name"]],
            on="product_code",
            how="left"
        )

        history_df = history_df[[
            "date",
            "product_name",
            "qty",
            "total"
        ]]

        st.dataframe(
            history_df.rename(columns={
                "date": "Date",
                "product_name": "Product",
                "qty": "Qty",
                "total": "Total"
            }),
            hide_index = True,
            use_container_width=True
        )

# ---------------- EXPENSES ----------------
with tab2:

    st.header("Cash Balance")
    balance = get_cash_balance()
    st.metric("Current Cash Balance", f"Rp {balance:,}")

    st.header("Expenses")

    expense_date = st.date_input("Expense Date", date.today())
    category = st.text_input("Category")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Add Expense"):
        add_expense(expense_date, category, description, amount)
        st.success("Expense added")

    expense_history_df = get_expense_history()

    st.dataframe(expense_history_df.style.format({"amount": "Rp {:,.0f}"}),
            use_container_width=True,
            hide_index= True)

with tab3:
    st.header("Reports")

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start date")
    with col2:
        end_date = st.date_input("End date")

    st.divider()

    # -------- SALES REPORT --------
    st.subheader("Sales Report")

    sales_df, total_qty, total_sales = get_sales_report_with_total(start_date, end_date)

    col1,col2 = st.columns(2)
    
    with col1:
        st.metric("Total Sales", f"Rp {total_sales:,.0f}")
    with col2:
        st.metric("Total Qty", total_qty)

    
    sales_df = get_sales_report(start_date, end_date)
    detailed_df = get_detailed_sales(start_date, end_date)

    summary_df = (
    sales_df
    .merge(menu, on="product_code", how="left")
    .groupby("product_name", as_index=False)
    .agg({
        "qty": "sum",
        "total": "sum"
    }))

    # Drop products with zero sales
    summary_df = summary_df[summary_df["qty"] > 0]

    if sales_df.empty:
        st.info("No sales data for selected period")
    else:
        st.dataframe(
            sales_df.style.format({"total": "Rp {:,.0f}"}),
            use_container_width=True,
            hide_index= True
        )

    if not sales_df.empty:
        pdf_bytes = generate_sales_summary_pdf(
        summary_df,
        start_date,
        end_date
    )

        st.download_button(
            label="🖨️ Download Sales Report (PDF)",
            data=pdf_bytes,
            file_name=f"sales_report_{start_date}_{end_date}.pdf",
            mime="application/pdf"
        )

    st.divider()

    st.subheader("Expense Report")

    expense_df = get_expense_report(start_date, end_date)

    if expense_df.empty:
        st.info("No expenses for selected period")
    else:
        st.dataframe(
            expense_df.style.format({"total_amount": "Rp {:,.0f}"}),
            use_container_width=True,
            hide_index= True
        )

    st.divider()

    # -------- CASHFLOW REPORT --------
    st.subheader("💰 Cashflow Summary")

    cashflow_df = get_cashflow_report(date(2026,1,1), date.today())

    st.dataframe(
        cashflow_df.style.format({"Amount": "Rp {:,.0f}"}),
        use_container_width=True,
        hide_index= True
    )

with tab4:
    
    st.header("Charts")
    st.subheader("Chart Date Range")

    start_date, end_date = st.date_input(
        "Select period",
        value=[date.today() - timedelta(days=6), date.today()]
    )

    sales_df = get_detailed_sales(start_date,end_date)
    sales_df["date"] = pd.to_datetime(sales_df["date"]).dt.date

    with st.container(border=True):
        st.subheader("Sales Trend")

        trend_df = (
            sales_df
            .groupby("date", as_index=False)["total"]
            .sum()
            .sort_values("date")
        )

        st.line_chart(
            trend_df.set_index("date")["total"]
        )

    with st.container(border=True):
        st.subheader("Sales Distribution")
        dist_df = (
        sales_df
        .groupby("product_name", as_index=False)["qty"]
        .sum()
        .sort_values("qty", ascending=False)
    )

        st.bar_chart(
        dist_df.set_index("product_name")["qty"]
        )