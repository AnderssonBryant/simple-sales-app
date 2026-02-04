import pandas as pd
import os
from datetime import date
from backend.menu import load_menu

SALES_FILE = "data/daily_sales.csv"

import pandas as pd
import os
from datetime import date
from backend.menu import load_menu


# =========================
# FILE INITIALIZATION
# =========================
def ensure_data_files():
    if not os.path.exists(SALES_FILE):
        pd.DataFrame(
            columns=["date", "product_code", "qty", "total"]
        ).to_csv(SALES_FILE, index=False)


# =========================
# BULK SALES CREATION
# =========================
def create_bulk_daily_sales(qty_by_product: dict, sale_date: date):
    """
    qty_by_product = {
        "LAT": 10,
        "ESP": 5,
        ...
    }
    """

    menu = load_menu()
    menu_map = (
        menu.set_index("product_code")["price"]
        .to_dict()
    )

    sales = []

    for product_code, qty in qty_by_product.items():
        if qty <= 0:
            continue  # ignore zero sales

        if product_code not in menu_map:
            raise ValueError(f"Invalid product code: {product_code}")

        total = int(menu_map[product_code]) * int(qty)

        sales.append({
            "date": sale_date.isoformat(),
            "product_code": product_code,
            "qty": int(qty),
            "total": total
        })

    return sales


# =========================
# BULK SAVE (UPSERT)
# =========================
def save_bulk_daily_sales(sales: list):
    """
    Upsert logic:
    - Same date + product_code → overwrite
    """
    ensure_data_files()

    df_existing = pd.read_csv(SALES_FILE)

    if df_existing.empty:
        df_new = pd.DataFrame(sales)
        df_new.to_csv(SALES_FILE, index=False)
        return

    # Remove rows that will be replaced
    for sale in sales:
        df_existing = df_existing[
            ~(
                (df_existing["date"] == sale["date"]) &
                (df_existing["product_code"] == sale["product_code"])
            )
        ]

    df_updated = pd.concat(
        [df_existing, pd.DataFrame(sales)],
        ignore_index=True
    )

    df_updated.to_csv(SALES_FILE, index=False)


# =========================
# AGGREGATION (REPORT USE)
# =========================
def get_sales_total(start_date=None, end_date=None):
    if not os.path.exists(SALES_FILE):
        return 0

    df = pd.read_csv(SALES_FILE)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    if start_date:
        df = df[df["date"] >= start_date]
    if end_date:
        df = df[df["date"] <= end_date]

    return int(df["total"].sum())


def get_sales_history():
    if not os.path.exists(SALES_FILE):
        return pd.DataFrame()

    df = pd.read_csv(SALES_FILE)
    df["date"] = pd.to_datetime(df["date"]).dt.date


    if df.empty:
        return pd.DataFrame()

    # Sort latest date first
    df = df.sort_values(
        by=["date", "product_code"],
        ascending=[False, True]
    )

    return df


def get_detailed_sales(start_date, end_date):
    df = pd.read_csv(SALES_FILE)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    df = df[
        (df["date"] >= start_date) &
        (df["date"] <= end_date) 
    ]

    menu = load_menu()

    df = df.merge(
        menu[["product_code", "product_name", "price"]],
        on="product_code",
        how="left"
    )

    return df[[
        "date",
        "product_name",
        "price",
        "qty",
        "total"
    ]]
