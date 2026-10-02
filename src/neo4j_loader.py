import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase


# Load environment variables
load_dotenv()


INPUT_PATH = "data/enriched_transactions.csv"

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Keep this small because Neo4j previously had memory issues
BATCH_SIZE = 100


def load_data():

    print("Loading enriched transactions...")

    df = pd.read_csv(INPUT_PATH)

    # Stable transaction IDs matching PostgreSQL
    df["transaction_id"] = df.index + 1

    print("Rows loaded:", len(df))

    return df


def create_constraints(session):

    print("Creating Neo4j constraints...")

    session.run("""
        CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
        FOR (c:Customer)
        REQUIRE c.customer_id IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT device_id_unique IF NOT EXISTS
        FOR (d:Device)
        REQUIRE d.device_id IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT ip_address_unique IF NOT EXISTS
        FOR (ip:IP)
        REQUIRE ip.ip_address IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT merchant_id_unique IF NOT EXISTS
        FOR (m:Merchant)
        REQUIRE m.merchant_id IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT transaction_id_unique IF NOT EXISTS
        FOR (t:Transaction)
        REQUIRE t.transaction_id IS UNIQUE
    """)

    print("Constraints created!")


def clear_graph(session):

    print("\nClearing existing Neo4j graph...")

    total_deleted = 0

    while True:

        result = session.run("""
            MATCH (n)
            WITH n
            LIMIT 1000
            DETACH DELETE n
            RETURN count(*) AS deleted
        """)

        deleted = result.single()["deleted"]

        total_deleted += deleted

        print(
            f"Deleted {deleted} nodes | "
            f"Total deleted: {total_deleted}"
        )

        if deleted == 0:
            break

    print("Existing Neo4j graph cleared!")


def insert_batch(session, batch):

    session.run(
        """
        UNWIND $rows AS row

        MERGE (c:Customer {
            customer_id: row.customer_id
        })

        MERGE (d:Device {
            device_id: row.device_id
        })

        MERGE (ip:IP {
            ip_address: row.ip_address
        })

        MERGE (m:Merchant {
            merchant_id: row.merchant_id
        })

        MERGE (t:Transaction {
            transaction_id: row.transaction_id
        })

        SET
            t.time = row.time,
            t.amount = row.amount,
            t.is_fraud = row.is_fraud

        MERGE (c)-[:USES_DEVICE]->(d)

        MERGE (c)-[:USES_IP]->(ip)

        MERGE (c)-[:TRANSACTS_WITH]->(m)

        MERGE (c)-[:MAKES]->(t)

        MERGE (t)-[:TRANSACTS_WITH]->(m)
        """,
        rows=batch
    )


def create_graph(df):

    print("\nConnecting to Neo4j...")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(
            NEO4J_USERNAME,
            NEO4J_PASSWORD
        )
    )

    try:

        with driver.session() as session:

            # Create constraints
            create_constraints(session)

            # IMPORTANT:
            # We changed the synthetic identity data,
            # so the old graph must be completely rebuilt.
            clear_graph(session)

            total_rows = len(df)

            print(
                f"\nStarting graph load: {total_rows:,} transactions"
            )

            for start in range(
                0,
                total_rows,
                BATCH_SIZE
            ):

                end = min(
                    start + BATCH_SIZE,
                    total_rows
                )

                batch_df = df.iloc[start:end]

                batch = batch_df[
                    [
                        "transaction_id",
                        "Time",
                        "Amount",
                        "Class",
                        "customer_id",
                        "device_id",
                        "ip_address",
                        "merchant_id"
                    ]
                ].rename(
                    columns={
                        "Time": "time",
                        "Amount": "amount",
                        "Class": "is_fraud"
                    }
                ).to_dict("records")

                insert_batch(
                    session,
                    batch
                )

                print(
                    f"Loaded {end:,} / "
                    f"{total_rows:,} transactions"
                )

        print("\nNeo4j graph rebuilt successfully!")

    finally:

        driver.close()


def main():

    df = load_data()

    create_graph(df)


if __name__ == "__main__":
    main()