from sqlalchemy import create_engine
from dotenv import load_dotenv

import pandas as pd
import os

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def create_tables():

    with engine.connect() as conn:

        with open("sql/schema.sql", "r") as file:
            sql = file.read()

        conn.exec_driver_sql(sql)

        conn.commit()

    print("Tablas creadas")


def load_data(final_df):

    # =========================
    # DIM PRODUCT
    # =========================

    dim_product = final_df[[
        "PCODE",
        "TYPE",
        "DESCRIP",
        "PRICE",
        "COST"
    ]].drop_duplicates()

    dim_product.columns = [
        "pcode",
        "tipo",
        "descripcion",
        "precio",
        "costo"
    ]

    dim_product.to_sql(
        "dim_product",
        engine,
        if_exists="append",
        index=False
    )

    # =========================
    # DIM SUPPLIER
    # =========================

    dim_supplier = final_df[[
        "SUPPLIER"
    ]].drop_duplicates()

    dim_supplier.columns = [
        "nombre"
    ]

    dim_supplier.to_sql(
        "dim_supplier",
        engine,
        if_exists="append",
        index=False
    )

    # =========================
    # DIM TIEMPO
    # =========================

    dim_tiempo = pd.DataFrame()

    dim_tiempo["fecha"] = final_df["DATE"]

    dim_tiempo["anio"] = final_df["DATE"].dt.year

    dim_tiempo["mes"] = final_df["DATE"].dt.month

    dim_tiempo["dia"] = final_df["DATE"].dt.day

    dim_tiempo = dim_tiempo.drop_duplicates()

    dim_tiempo.to_sql(
        "dim_tiempo",
        engine,
        if_exists="append",
        index=False
    )

    # =========================
    # LEER DIMENSIONES DESDE DB
    # =========================

    products_db = pd.read_sql(
        "SELECT * FROM dim_product",
        engine
    )

    suppliers_db = pd.read_sql(
        "SELECT * FROM dim_supplier",
        engine
    )

    tiempo_db = pd.read_sql(
        "SELECT * FROM dim_tiempo",
        engine
    )

    # =========================
    # MAP PRODUCT_ID
    # =========================

    fact_df = final_df.merge(
        products_db,
        left_on="PCODE",
        right_on="pcode",
        how="left"
    )

    fact_df = fact_df.rename(
        columns={
            "id": "product_id"
        }
    )

    # =========================
    # MAP SUPPLIER_ID
    # =========================

    fact_df = fact_df.merge(
        suppliers_db,
        left_on="SUPPLIER",
        right_on="nombre",
        how="left"
    )

    fact_df = fact_df.rename(
        columns={
            "id": "supplier_id"
        }
    )

    # =========================
    # MAP DATE_ID
    # =========================

    tiempo_db["fecha"] = pd.to_datetime(
        tiempo_db["fecha"]
    )

    fact_df = fact_df.merge(
        tiempo_db,
        left_on="DATE",
        right_on="fecha",
        how="left"
    )

    fact_df = fact_df.rename(
        columns={
            "id": "date_id"
        }
    )

    # =========================
    # FACT TABLE
    # =========================

    fact_sales = pd.DataFrame()

    fact_sales["product_id"] = fact_df["product_id"]

    fact_sales["supplier_id"] = fact_df["supplier_id"]

    fact_sales["date_id"] = fact_df["date_id"]

    fact_sales["cantidad"] = fact_df["QTY"]

    fact_sales["costo"] = (
        fact_df["COST"] * fact_df["QTY"]
    )

    fact_sales["ganancia"] = (
        (fact_df["PRICE"] - fact_df["COST"])
        * fact_df["QTY"]
    )

    fact_sales.to_sql(
        "fact_sales",
        engine,
        if_exists="append",
        index=False
    )

    print("Datos cargados correctamente")
