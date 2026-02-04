import pandas as pd
from datetime import date
from backend.menu import load_menu
import os

from backend.cash import get_opening_balance
from backend.sales import get_sales_total
from backend.expenses import get_expenses_total


SALES_PATH = "data/daily_sales.csv"
EXPENSE_FILE = "data/expenses.csv"

def get_sales_report(start_date, end_date):
    if not os.path.exists(SALES_PATH):
        return pd.DataFrame()

    sales = pd.read_csv(SALES_PATH)
    sales["date"] = pd.to_datetime(sales["date"]).dt.date

    sales = sales[
        (sales["date"] >= start_date) &
        (sales["date"] <= end_date)
    ]

    if sales.empty:
        return pd.DataFrame()

    summary = (
        sales.groupby("product_code", as_index=False)
        .agg(
            qty=("qty", "sum"),
            total=("total", "sum")
        )
    )

    # 🔑 Remove zero-qty products
    summary = summary[summary["qty"] > 0]

    if summary.empty:
        return pd.DataFrame()

    menu = load_menu()

    report = summary.merge(
        menu[["product_code", "product_name"]],
        on="product_code",
        how="left"
    )

    return report[[
        "product_name",
        "qty",
        "total"
    ]]


def cashflow_between(start_date: date, end_date: date):
    sales = pd.read_csv("data/daily_sales.csv")
    expenses = pd.read_csv("data/expenses.csv")

    sales_mask = (
        (sales["date"] >= start_date.isoformat()) &
        (sales["date"] <= end_date.isoformat())
    )
    expenses_mask = (
        (expenses["date"] >= start_date.isoformat()) &
        (expenses["date"] <= end_date.isoformat())
    )

    total_inflow = int(sales.loc[sales_mask, "total"].sum())
    total_outflow = int(expenses.loc[expenses_mask, "amount"].sum())

    return {
        "inflow": total_inflow,
        "outflow": total_outflow,
        "net_cashflow": total_inflow - total_outflow
    }

def get_cashflow_report(start_date, end_date):
    opening = get_opening_balance()
    sales = get_sales_total(start_date, end_date)
    expenses = get_expenses_total(start_date, end_date)
    balance = opening + sales - expenses

    return pd.DataFrame([
        {"Description": "Opening Balance", "Amount": opening},
        {"Description": "Total Sales", "Amount": sales},
        {"Description": "Total Expenses", "Amount": expenses},
        {"Description": "Final Cash Balance", "Amount": balance},
    ])


def get_expense_report(start_date, end_date):
    if not os.path.exists(EXPENSE_FILE):
        return pd.DataFrame()

    expenses = pd.read_csv(EXPENSE_FILE)
    expenses["date"] = pd.to_datetime(expenses["date"]).dt.date

    expenses = expenses[
        (expenses["date"] >= start_date) &
        (expenses["date"] <= end_date)
    ]

    if expenses.empty:
        return pd.DataFrame()

    # Aggregate by category (recommended)
    report = (
        expenses.groupby("category", as_index=False)
        .agg(
            total_amount=("amount", "sum")
        )
    )

    # Remove zero totals (safety)
    report = report[report["total_amount"] > 0]

    return report


def get_sales_report_with_total(start_date, end_date):
    df = get_sales_report(start_date, end_date)

    if df.empty:
        return df, 0, 0

    grand_total = df["total"].sum()
    total_qty = df["qty"].sum()

    return df, total_qty, grand_total

