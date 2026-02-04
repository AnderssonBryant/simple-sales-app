import pandas as pd
import os
from datetime import date

EXPENSE_FILE = "data/expenses.csv"

def ensure_expense_file():
    if not os.path.exists(EXPENSE_FILE):
        pd.DataFrame(
            columns=["date", "category", "description", "amount"]
        ).to_csv(EXPENSE_FILE, index=False)

def add_expense(expense_date: date, category: str, description: str, amount: int):
    ensure_expense_file()

    if amount <= 0:
        raise ValueError("Amount must be positive")

    df = pd.read_csv(EXPENSE_FILE)

    new_row = {
        "date": expense_date.isoformat(),
        "category": category,
        "description": description,
        "amount": amount
    }

    df = pd.concat([df, pd.DataFrame([new_row])])
    df.to_csv(EXPENSE_FILE, index=False)

def get_expenses_total(start_date=None, end_date=None):
    if not os.path.exists(EXPENSE_FILE):
        return 0

    df = pd.read_csv(EXPENSE_FILE)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    if start_date:
        df = df[df["date"] >= start_date]
    if end_date:
        df = df[df["date"] <= end_date]

    return int(df["amount"].sum())


def get_expense_history():
    if not os.path.exists(EXPENSE_FILE):
        return pd.DataFrame()

    df = pd.read_csv(EXPENSE_FILE)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    if df.empty:
        return pd.DataFrame()

    # Sort latest date first
    df = df.sort_values(
        by=["date"],
        ascending=[False]
    )

    return df