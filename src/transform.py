import pandas as pd


def clean_columns(df):
    """
    Normaliza nombres de columnas:
    - elimina espacios
    - convierte a mayúsculas
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
    )

    return df


def clean_qty(df):
    """
    Convierte QTY a numérico.
    Valores inválidos -> NaN
    """
    if "QTY" in df.columns:
        df["QTY"] = pd.to_numeric(
            df["QTY"],
            errors="coerce"
        )

    return df


def clean_dates(df, dataset_name=None):
    """
    Convierte DATE a datetime según el dataset.
    """

    if "DATE" not in df.columns:
        return df

    # Catalog_Orders.txt
    # formato: month/year/day
    # ejemplo: 3/97/7 00:00:00
    if dataset_name == "catalog":

        df["DATE"] = pd.to_datetime(
            df["DATE"],
            format="%m/%y/%d %H:%M:%S",
            errors="coerce"
        )

    # Web_orders.txt
    # formato: day/month/year
    # ejemplo: 17/12/2000 00:00:00
    elif dataset_name == "web":

        df["DATE"] = pd.to_datetime(
            df["DATE"],
            format="%d/%m/%Y %H:%M:%S",
            errors="coerce"
        )

    else:
        df["DATE"] = pd.to_datetime(
            df["DATE"],
            errors="coerce"
        )

    return df


def clean_catalog(df):
    """
    Normaliza valores de CATALOG.
    """

    if "CATALOG" in df.columns:

        df["CATALOG"] = (
            df["CATALOG"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    return df


def remove_duplicates(df):
    """
    Elimina registros duplicados.
    """

    return df.drop_duplicates()


def remove_nulls(df):
    """
    Elimina filas completamente vacías.
    """

    return df.dropna(how="all")


def transform(catalog, web, products):
    """
    Pipeline de transformación ETL.
    """

    # =========================
    # CLEAN CATALOG
    # =========================

    catalog = clean_columns(catalog)
    catalog = clean_qty(catalog)
    catalog = clean_dates(catalog, "catalog")
    catalog = clean_catalog(catalog)
    catalog = remove_duplicates(catalog)
    catalog = remove_nulls(catalog)

    # =========================
    # CLEAN WEB
    # =========================

    web = clean_columns(web)
    web = clean_qty(web)
    web = clean_dates(web, "web")
    web = clean_catalog(web)
    web = remove_duplicates(web)
    web = remove_nulls(web)

    # =========================
    # CLEAN PRODUCTS
    # =========================

    products = clean_columns(products)
    products = remove_duplicates(products)
    products = remove_nulls(products)

    # =========================
    # INTEGRATE ORDERS
    # =========================

    orders = pd.concat(
        [catalog, web],
        ignore_index=True
    )

    # =========================
    # JOIN PRODUCTS
    # =========================

    final_df = orders.merge(
        products,
        on="PCODE",
        how="left"
    )

    return final_df
