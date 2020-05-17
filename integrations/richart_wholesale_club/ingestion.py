import os

import numpy as np
import pandas as pd

from models import BranchProduct, Product

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
PRODUCTS_PATH = os.path.join(ASSETS_DIR, "PRODUCTS.csv")
STOCK_PATH = os.path.join(ASSETS_DIR, "STOCK.csv")


def process_csv_files():
    products_df = pd.read_csv(filepath_or_buffer=PRODUCTS_PATH, sep="|",)
    stock_df = pd.read_csv(filepath_or_buffer=STOCK_PATH, sep="|",)


if __name__ == "__main__":
    process_csv_files()
