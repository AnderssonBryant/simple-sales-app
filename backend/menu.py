import pandas as pd

MENU_PATH = "data/menu.csv"

def load_menu():
    return pd.read_csv(MENU_PATH)

def get_price(product_code):
    menu = load_menu()
    row = menu.loc[menu["product_code"] == product_code]

    if row.empty:
        raise ValueError("Invalid product code")

    return int(row.iloc[0]["price"])
