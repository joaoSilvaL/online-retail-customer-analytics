
from pathlib import Path

import pandas as pd
import sqlalchemy

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data/database/online_retail.db"
QUERY_PATH = BASE_DIR / "sql/analytics/customer_rfm.sql"

REFERENCE_DATE = "2011-12-10"


def import_query(path):
    with open(path, encoding="utf-8") as file:
        return file.read()


def load_customer_data():

    engine = sqlalchemy.create_engine(
        f"sqlite:///{DB_PATH.as_posix()}"
    )

    try:
        query = import_query(QUERY_PATH)

        df = pd.read_sql(
            sqlalchemy.text(query),
            engine,
            params={"reference_date": REFERENCE_DATE}
        )

        return df

    finally:
        engine.dispose()


def main():

    df = load_customer_data()

    print(df.head())
    print(df.describe())

    features = [
        "recency",
        "frequency",
        "monetary"
    ]

    X = df[features].copy()

    X = X.apply(lambda col: __import__("numpy").log1p(col))

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    df["cluster"] = kmeans.fit_predict(X_scaled)

    score = silhouette_score(X_scaled, df["cluster"])

    print(f"\nSilhouette Score: {score:.4f}")

    print("\nPerfil dos clusters:")

    print(
        df.groupby("cluster")[features]
        .mean()
        .round(2)
    )

    print("\nQuantidade de clientes por cluster:")

    print(df["cluster"].value_counts().sort_index())

    pca = PCA(n_components=2)

    X_pca = pca.fit_transform(X_scaled)

    df["pca_1"] = X_pca[:, 0]
    df["pca_2"] = X_pca[:, 1]

    sns.scatterplot(
        data=df,
        x="pca_1",
        y="pca_2",
        hue="cluster",
        palette="deep"
    )

    plt.title("Segmentação de clientes - K-Means")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
