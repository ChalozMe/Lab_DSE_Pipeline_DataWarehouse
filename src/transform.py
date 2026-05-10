import pandas as pd


def clean_columns(df):
    """
    Normaliza nombres de columnas:
    - elimina espacios
    - convierte a mayúsculas
    """
    df.columns = df.columns.str.strip().str.upper()
    return df


def clean_qty(df):
    """
    Convierte QTY a numérico.
    Valores inválidos -> NaN
    """
    if "QTY" in df.columns:
        df["QTY"] = pd.to_numeric(df["QTY"], errors="coerce")

    return df


def clean_dates(df):
    """
    Convierte DATE a datetime.
    Fechas inválidas -> NaT
    """
    if "DATE" in df.columns:
        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

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


    datasets = [catalog, web, products]

    cleaned = []

    for df in datasets:
        df = clean_columns(df)
        df = clean_qty(df)
        df = clean_dates(df)
        df = clean_catalog(df)
        df = remove_duplicates(df)
        df = remove_nulls(df)

        cleaned.append(df)

    catalog_clean, web_clean, products_clean = cleaned

    # =========================
    # INTEGRACIÓN
    # =========================

    # Unir órdenes catalog + web
    orders = pd.concat(
        [catalog_clean, web_clean],
        ignore_index=True
    )

    # Unir con productos usando PCODE
    final_df = orders.merge(
        products_clean,
        on="PCODE",
        how="left"
    )

    return final_df
