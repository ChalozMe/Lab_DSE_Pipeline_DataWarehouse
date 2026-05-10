import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()


def create_connection():

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    return conn

def load(df):
    """
    Carga DataFrame final a PostgreSQL.
    """

    conn = create_connection()
    cursor = conn.cursor()

    # =========================
    # INSERTS
    # =========================

    for _, row in df.iterrows():

        cursor.execute(
            """
            INSERT INTO sales_fact (
                id_x,:
                inv,
                date,
                catalog,
                pcode,
                qty,
                custnum,
                type,
                descrip,
                price,
                cost,
                supplier
            )
            VALUES (%s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s)
            """,
            (
                row.get("ID"),
                row.get("INV"),
                row.get("DATE"),
                row.get("CATALOG"),
                row.get("PCODE"),
                row.get("QTY"),
                row.get("CUSTNUM"),
                row.get("TYPE"),
                row.get("DESCRIP"),
                row.get("PRICE"),
                row.get("COST"),
                row.get("SUPPLIER")
            )
        )

    conn.commit()

    cursor.close()
    conn.close()

    print("Datos cargados correctamente.")
