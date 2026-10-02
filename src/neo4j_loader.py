import pandas as pd
from neo4j import GraphDatabase


INPUT_PATH = "data/enriched_transactions.csv"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "credixis123"

BATCH_SIZE = 5000


def load_data():
    print("Loading enriched transactions...")

    df = pd.read_csv(INPUT_PATH)

    # Create stable transaction IDs matching PostgreSQL's 1-based IDs
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
    print("Clearing existing Neo4j graph...")

    session.run("""
        MATCH (n)
        DETACH DELETE n
    """)

    print("Existing graph cleared!")


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

    print("Connecting to Neo4j...")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    with driver.session() as session:

        create_constraints(session)

        clear_graph(session)

        total_rows = len(df)

        for start in range(0, total_rows, BATCH_SIZE):

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

            insert_batch(session, batch)

            print(
                f"Loaded {end:,} / {total_rows:,} transactions"
            )

    driver.close()

    print("Neo4j graph created successfully!")


def main():

    df = load_data()

    create_graph(df)


if __name__ == "__main__":
    main()