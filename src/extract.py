import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract():
    catalog = pd.read_csv(os.path.join(BASE_DIR, "data/raw/Catalog_Orders.txt"))

    web = pd.read_csv(
    os.path.join(BASE_DIR, "data/raw/Web_orders.txt"),
    sep=";",
    header=0,
    names=[
        "ID",
        "INV",
        "PCODE",
        "DATE",
        "CATALOG",
        "QTY",
        "CUSTOMER"
    ],
    quotechar='"'
)

    products = pd.read_csv(os.path.join(BASE_DIR, "data/raw/products.txt"))

    return catalog, web, products


if __name__ == "__main__":
    c, w, p = extract()

    print("Catalog:")
    print(c.head())

    print("\nWeb:")
    print(w.head())

    print("\nProducts:")
    print(p.head())
