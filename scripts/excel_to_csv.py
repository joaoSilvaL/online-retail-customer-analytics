
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

EXCEL_PATH = BASE_DIR / "data/raw/online_retail_II.xlsx"
CSV_PATH = BASE_DIR / "data/processed/online_retail_II.csv"

CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

sheets = pd.read_excel(
    EXCEL_PATH,
    sheet_name=None,
    dtype={
        "Invoice": "string",
        "StockCode": "string",
        "Customer ID": "string"
    }
)

for sheet_name, df in sheets.items():
    print(f"\nPlanilha: {sheet_name}")
    print(f"Registros: {len(df)}")
    print(f"Colunas: {df.columns.tolist()}")

df = pd.concat(sheets.values(), ignore_index=True)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

columns = [
    "invoice",
    "stockcode",
    "description",
    "quantity",
    "invoicedate",
    "price",
    "customer_id",
    "country"
]

df = df[columns]

df["invoicedate"] = pd.to_datetime(df["invoicedate"])

df.to_csv(
    CSV_PATH,
    index=False,
    encoding="utf-8"
)

print("\nConversão concluída!")
print(f"Total de registros: {len(df)}")
print(f"Arquivo gerado: {CSV_PATH}")

print("\nPrimeiros registros:")
print(df.head())

print("\nInformações:")
print(df.info())
