import os

import numpy as np
import pandas as pd
import sqlite3

from models import BranchProduct, Product

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
PRODUCTS_PATH = os.path.join(ASSETS_DIR, "PRODUCTS.csv")
STOCK_PATH = os.path.join(ASSETS_DIR, "STOCK.csv")
DB_PATH = os.path.join(PROJECT_DIR, "db.sqlite")

accepted_branches = ['MM', 'RHSM']


def process_csv_files():
    products_df = pd.read_csv(filepath_or_buffer=PRODUCTS_PATH, sep="|",)
    stock_df = pd.read_csv(filepath_or_buffer=STOCK_PATH, sep="|",)
    load_products_to_db(stock_df)


def load_products_to_db(stock_df):
    # for index, row in stock_df.iterrows():
    #     if str(row['BRANCH']).upper() in accepted_branches:
    #         print(row['SKU'], row['BRANCH'], row['STOCK'])
    create_connection()


def create_connection():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.fetchall()
    cursor.execute("""SELECT * FROM products;""")
    conn.close()


if __name__ == "__main__":
    process_csv_files()
