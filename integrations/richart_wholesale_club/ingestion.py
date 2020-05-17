import os

import numpy as np
import pandas as pd
import sqlite3
from itertools import islice

from models import BranchProduct, Product

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
PRODUCTS_PATH = os.path.join(ASSETS_DIR, "PRODUCTS.csv")
STOCK_PATH = os.path.join(ASSETS_DIR, "STOCK.csv")
DB_PATH = os.path.join(PROJECT_DIR, "db.sqlite")

accepted_branches = ['MM', 'RHSM']
conn = None
cursor = None


def process_csv_files():
    products_df = pd.read_csv(filepath_or_buffer=PRODUCTS_PATH, sep="|", )
    stock_df = pd.read_csv(filepath_or_buffer=STOCK_PATH, sep="|", )
    load_stocks_to_db(stock_df)


def load_stocks_to_db(stock_df):
    create_connection()
    for index, row in islice(stock_df.iterrows(), 20):
        if str(row['BRANCH']).upper() in accepted_branches:
            insert_stock(row['SKU'], row['BRANCH'], row['PRICE'], row['STOCK'])


def create_connection():
    global conn
    global cursor
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


def insert_stock(sku, branch, price, stock):
    global cursor
    # Insert if the product does not exits, otherwise update the current stock
    cursor.execute("""INSERT OR REPLACE INTO branchproducts (id, product_id, branch, stock, price) VALUES 
                    ((SELECT id FROM branchproducts where product_id = ? ), ?, ?, ?, ?)""",
                   (sku, sku, str(branch).strip().upper(), price, stock))
    conn.commit()
    # print(f'inserted {sku} from {branch}')


def close_connection():
    global conn
    conn.close()


if __name__ == "__main__":
    process_csv_files()
