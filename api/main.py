import os
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI

from neo4j import GraphDatabase


# Load environment variables
load_dotenv()


# ============================================================
# PostgreSQL configuration
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")


# ============================================================
# Neo4j configuration
# ============================================================

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


neo4j_driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(
        NEO4J_USERNAME,
        NEO4J_PASSWORD
    )
)


# ============================================================
# FastAPI
# ============================================================

app = FastAPI(
    title="Credixis Risk API"
)


# ============================================================
# PostgreSQL connection
# ============================================================

def get_connection():

    return psycopg2.connect(
        DATABASE_URL
    )


# ============================================================
# Home
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Credixis Risk API is running"
    }


# ============================================================
# Get latest risk results
# ============================================================

@app.get("/risk-results")
def get_risk_results():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            risk_id,
            transaction_id,
            customer_id,
            device_id,
            amount,
            risk_score,
            risk_level,
            is_fraud,
            processed_at
        FROM risk_results
        ORDER BY risk_id DESC
        LIMIT 100
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    results = []

    for row in rows:

        results.append({

            "risk_id": row[0],

            "transaction_id": row[1],

            "customer_id": row[2],

            "device_id": row[3],

            "amount": float(row[4]),

            "risk_score": row[5],

            "risk_level": row[6],

            "is_fraud": row[7],

            "processed_at": row[8]
        })

    return {

        "count": len(results),

        "results": results
    }


# ============================================================
# Get high-risk transactions
# ============================================================

@app.get("/risk-results/high")
def get_high_risk_results():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            risk_id,
            transaction_id,
            customer_id,
            device_id,
            amount,
            risk_score,
            risk_level,
            is_fraud,
            processed_at
        FROM risk_results
        WHERE risk_level = 'HIGH'
        ORDER BY risk_score DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    results = []

    for row in rows:

        results.append({

            "risk_id": row[0],

            "transaction_id": row[1],

            "customer_id": row[2],

            "device_id": row[3],

            "amount": float(row[4]),

            "risk_score": row[5],

            "risk_level": row[6],

            "is_fraud": row[7],

            "processed_at": row[8]
        })

    return {

        "count": len(results),

        "results": results
    }


# ============================================================
# Get risk for a specific transaction
# ============================================================

@app.get("/risk-results/{transaction_id}")
def get_transaction_risk(
    transaction_id: int
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            risk_id,
            transaction_id,
            customer_id,
            device_id,
            ip_address,
            merchant_id,
            amount,
            risk_score,
            risk_level,
            is_fraud,
            processed_at
        FROM risk_results
        WHERE transaction_id = %s
        ORDER BY risk_id DESC
        LIMIT 1
    """, (transaction_id,))

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:

        return {
            "message": "Transaction not found"
        }

    return {

        "risk_id": row[0],

        "transaction_id": row[1],

        "customer_id": row[2],

        "device_id": row[3],

        "ip_address": row[4],

        "merchant_id": row[5],

        "amount": float(row[6]),

        "risk_score": row[7],

        "risk_level": row[8],

        "is_fraud": row[9],

        "processed_at": row[10]
    }


# ============================================================
# Customer identity graph
# ============================================================

@app.get("/customers/{customer_id}/connections")
def get_customer_connections(
    customer_id: str
):

    with neo4j_driver.session() as session:

        result = session.run("""

            MATCH (
                c:Customer {
                    customer_id: $customer_id
                }
            )

            OPTIONAL MATCH
                (c)-[:USES_DEVICE]->(d:Device)

            WITH
                c,
                collect(DISTINCT d.device_id) AS devices

            OPTIONAL MATCH
                (c)-[:USES_IP]->(ip:IP)

            WITH
                c,
                devices,
                collect(DISTINCT ip.ip_address) AS ip_addresses

            OPTIONAL MATCH
                (c)-[:TRANSACTS_WITH]->(m:Merchant)

            WITH
                c,
                devices,
                ip_addresses,
                collect(DISTINCT m.merchant_id) AS merchants

            OPTIONAL MATCH
                (c)-[:USES_DEVICE]->(shared_device:Device)
                <-[:USES_DEVICE]-(other_customer:Customer)

            WHERE
                other_customer IS NOT NULL
                AND other_customer.customer_id <> $customer_id

            WITH
                c,
                devices,
                ip_addresses,
                merchants,
                other_customer,
                collect(
                    DISTINCT shared_device.device_id
                )[..10] AS shared_devices

            OPTIONAL MATCH
                (other_customer)-[:MAKES]->(t:Transaction)

            WITH
                c,
                devices,
                ip_addresses,
                merchants,
                other_customer,
                shared_devices,
                count(
                    CASE
                        WHEN t.is_fraud = 1
                        THEN 1
                    END
                ) AS fraud_transactions

            RETURN
                c.customer_id AS customer_id,

                devices,

                ip_addresses,

                merchants,

                collect({
                    customer_id:
                        other_customer.customer_id,

                    shared_devices:
                        shared_devices,

                    fraud_transactions:
                        fraud_transactions
                })[..50] AS connected_customers

        """, customer_id=customer_id)

        record = result.single()


    if record is None:

        return {
            "message": "Customer not found"
        }


    return {

        "customer_id":
            record["customer_id"],

        "devices":
            record["devices"],

        "ip_addresses":
            record["ip_addresses"],

        "merchants":
            record["merchants"],

        "connected_customers":
            record["connected_customers"]
    }

@app.get("/fraud-investigation/{customer_id}")
def fraud_investigation(customer_id: str):

    with neo4j_driver.session() as session:

        result = session.run("""
            MATCH (c:Customer {customer_id: $customer_id})

            OPTIONAL MATCH
                (c)-[:USES_DEVICE]->(d:Device)
                <-[:USES_DEVICE]-(other:Customer)

            WHERE other IS NOT NULL
              AND other.customer_id <> $customer_id

            OPTIONAL MATCH
                (other)-[:MAKES]->(t:Transaction)

            WITH
                c,
                other,
                collect(DISTINCT d.device_id) AS shared_devices,
                count(
                    CASE
                        WHEN t.is_fraud = 1
                        THEN 1
                    END
                ) AS fraud_transactions

            RETURN
                c.customer_id AS customer_id,
                collect({
                    connected_customer: other.customer_id,
                    shared_devices: shared_devices,
                    fraud_transactions: fraud_transactions
                })[..20] AS connections
        """, customer_id=customer_id)

        record = result.single()

    if record is None:
        return {
            "message": "Customer not found"
        }

    return {
        "customer_id": record["customer_id"],
        "connections": record["connections"]
    }

