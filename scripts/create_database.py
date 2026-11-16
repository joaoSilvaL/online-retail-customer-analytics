
from pathlib import Path

import pandas as pd
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.types import Text, Float
from tqdm import tqdm


BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "data/processed/online_retail_II.csv"
DB_PATH = BASE_DIR / "data/database/online_retail.db"

CHUNK_SIZE = 25000


def create_database():

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado: {CSV_PATH}"
        )

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    engine = sqlalchemy.create_engine(
        f"sqlite:///{DB_PATH.as_posix()}"
    )

    column_types = {
        "invoice": Text(),
        "stockcode": Text(),
        "description": Text(),
        "quantity": Float(),
        "invoicedate": Text(),
        "price": Float(),
        "customer_id": Text(),
        "country": Text()
    }

    chunks = pd.read_csv(
        CSV_PATH,
        dtype={
            "invoice": "string",
            "stockcode": "string",
            "customer_id": "string"
        },
        chunksize=CHUNK_SIZE
    )

    total_records = 0

    try:
        for i, df in enumerate(
            tqdm(chunks, desc="Importando dados")
        ):

            df.to_sql(
                name="transactions",
                con=engine,
                index=False,
                if_exists="replace" if i == 0 else "append",
                dtype=column_types
            )

            total_records += len(df)

        with engine.begin() as connection:

            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_customer
                ON transactions(customer_id)
            """))

            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_invoice_date
                ON transactions(invoicedate)
            """))

            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_invoice
                ON transactions(invoice)
            """))

        print("\nBanco criado com sucesso!")

        print(f"Registros importados: {total_records}")
        print(f"Localização: {DB_PATH}")

    finally:
        engine.dispose()


if __name__ == "__main__":
    create_database()
