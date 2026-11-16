
from pathlib import Path
import argparse

import pandas as pd
import sqlalchemy
from sqlalchemy import text


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data/database/online_retail.db"
SQL_DIR = BASE_DIR / "sql"


def import_query(path):
    """Lê uma consulta SQL de um arquivo."""
    with open(path, encoding="utf-8") as file:
        return file.read()


def execute_query(query_name, params=None):
    """Executa uma consulta SQL e exibe o resultado."""

    query_path = SQL_DIR / query_name

    if not query_path.exists():
        raise FileNotFoundError(
            f"Arquivo SQL não encontrado: {query_path}"
        )

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Banco de dados não encontrado: {DB_PATH}"
        )

    query = import_query(query_path)

    engine = sqlalchemy.create_engine(
        f"sqlite:///{DB_PATH.as_posix()}"
    )

    try:
        df = pd.read_sql(
            text(query),
            engine,
            params=params
        )

        print(f"\nConsulta: {query_name}")
        print(f"Registros retornados: {len(df)}")
        print("\nResultado:")
        print(df.to_string(index=False))

        return df

    finally:
        engine.dispose()


def main():

    parser = argparse.ArgumentParser(
        description="Executa consultas SQL no Online Retail II"
    )

    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Caminho da consulta SQL relativo à pasta sql"
    )

    parser.add_argument(
        "--date",
        type=str,
        help="Data de referência no formato YYYY-MM-DD"
    )

    args = parser.parse_args()

    params = {}

    if args.date:
        params["reference_date"] = args.date

    execute_query(args.query, params=params)


if __name__ == "__main__":
    main()
