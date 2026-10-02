import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATA_PATH = "data/creditcard.csv"


def load_data():
    print("Loading CSV...")

    df = pd.read_csv(DATA_PATH)

    print("Rows loaded:", len(df))

    return df


def insert_data(df):
    print("Connecting to PostgreSQL...")

    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    print("Clearing existing transactions...")

    cursor.execute(
        "TRUNCATE TABLE transactions RESTART IDENTITY;"
    )

    connection.commit()

    columns = [
        "Time",
        "Amount",
        *[f"V{i}" for i in range(1, 29)],
        "Class"
    ]

    df["Class"] = df["Class"].astype(bool)

    values = df[columns].values.tolist()

    insert_query = """
        INSERT INTO transactions (
            transaction_time,
            amount,
            v1, v2, v3, v4, v5, v6, v7, v8,
            v9, v10, v11, v12, v13, v14, v15, v16,
            v17, v18, v19, v20, v21, v22, v23, v24,
            v25, v26, v27, v28,
            is_fraud
        )
        VALUES %s
    """

    print("Inserting data...")

    execute_values(
        cursor,
        insert_query,
        values,
        page_size=5000
    )

    connection.commit()

    print("Data inserted successfully!")

    cursor.close()
    connection.close()


def main():
    df = load_data()
    insert_data(df)


if __name__ == "__main__":
    main()