import os
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Credixis Risk API")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.get("/")
def home():
    return {
        "message": "Credixis Risk API is running"
    }


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
@app.get("/risk-results/{transaction_id}")
def get_transaction_risk(transaction_id: int):
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