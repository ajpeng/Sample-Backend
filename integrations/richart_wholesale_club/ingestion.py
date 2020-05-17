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
    load_products_to_db(products_df)
    close_connection()


def load_stocks_to_db(stock_df):
    create_connection()
    for index, row in islice(stock_df.iterrows(), 50):
        if str(row['BRANCH']).upper() in accepted_branches and row['STOCK'] > 0:
            upsert_stock(row['SKU'], row['BRANCH'], row['PRICE'], row['STOCK'])


def load_products_to_db(products_df):
    for index, row in islice(products_df.iterrows(), 50):
        category = ''
        category = category + row['CATEGORY'] + '|' if row['CATEGORY'] else category
        category = category + row['SUB_CATEGORY'] + '|' if row['SUB_CATEGORY'] else category
        category = category + row['SUB_SUB_CATEGORY'] + '|' if row['SUB_SUB_CATEGORY'] else category
        # no category column in db
        # todo add package information
        upsert_product(row['SKU'], row['BARCODES'], row['BRAND'],  row['NAME'], row['DESCRIPTION'], '', row['IMAGE_URL'])


def create_connection():
    global conn
    global cursor
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


def upsert_stock(sku, branch, price, stock):
    global cursor
    # Insert if the stock does not exits, otherwise update the current stock
    cursor.execute("""INSERT OR REPLACE INTO branchproducts (id, product_id, branch, stock, price) VALUES 
                    ((SELECT id FROM branchproducts where product_id = ? ), ?, ?, ?, ?)""",
                   (sku, sku, str(branch).strip().upper(), price, stock))
    conn.commit()


def upsert_product(sku, barcodes, brand, name, description, package, image_url):
    cursor.execute("""INSERT OR REPLACE INTO products (id, sku, store, barcodes, brand, name, description, package, image_url) VALUES 
                        ((SELECT id FROM products where sku = ? ), 'Richart\'\'s' , ?, ?, ?, ?, ?, ?, ?)""",
                   (sku, sku, barcodes, brand, name, description, package, image_url))
    conn.commit()


def close_connection():
    global conn
    conn.close()


if __name__ == "__main__":
    process_csv_files()
