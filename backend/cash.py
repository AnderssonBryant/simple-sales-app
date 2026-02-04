import pandas as pd
import os
from datetime import date
from backend.sales import get_sales_total
from backend.expenses import get_expenses_total

CASH_FILE = "data/cash_events.csv"

def ensure_cash_file():
    if not os.path.exists(CASH_FILE):
        pd.DataFrame(
            columns=["date", "type", "description", "amount"]
        ).to_csv(CASH_FILE, index=False)

def set_opening_balance(opening_date: date, amount: int):
    ensure_cash_file()

    df = pd.read_csv(CASH_FILE)

    if "opening_balance" in df["type"].values:
        raise ValueError("Opening balance already exists")

    new_row = {
        "date": opening_date.isoformat(),
        "type": "opening_balance",
        "description": "Initial cash",
        "amount": int(amount)
    }

    df = pd.concat([df, pd.DataFrame([new_row])])
    df.to_csv(CASH_FILE, index=False)

def get_opening_balance():
    if not os.path.exists(CASH_FILE):
        return 0

    df = pd.read_csv(CASH_FILE)
    opening = df[df["type"] == "opening_balance"]

    if opening.empty:
        return 0

    return int(opening.iloc[0]["amount"])

def get_cash_balance(start_date=None, end_date=None):
    opening = get_opening_balance()
    sales = get_sales_total(start_date, end_date)
    expenses = get_expenses_total(start_date, end_date)

    return opening + sales - expenses
