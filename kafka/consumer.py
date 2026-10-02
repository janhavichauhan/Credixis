import json
import os
import psycopg2
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
KAFKA_TOPIC = "credit_transactions"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="credixis-risk-db-consumer",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()

def calculate_risk(transaction):
    score = 0

    if transaction["amount"] > 500:
        score += 20

    if transaction["amount"] > 200:
        score += 15

    if transaction["is_fraud"] == 1:
        score += 25

    if score >= 40:
        risk_level = "HIGH"
    elif score >= 20:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return score, risk_level

print("Kafka risk consumer started...")
print("Waiting for transactions...")

for message in consumer:
    transaction = message.value

    risk_score, risk_level = calculate_risk(transaction)

    cursor.execute(
        """
        INSERT INTO risk_results (
            transaction_id,
            customer_id,
            device_id,
            ip_address,
            merchant_id,
            amount,
            risk_score,
            risk_level,
            is_fraud
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            transaction["transaction_id"],
            transaction["customer_id"],
            transaction["device_id"],
            transaction["ip_address"],
            transaction["merchant_id"],
            transaction["amount"],
            risk_score,
            risk_level,
            bool(transaction["is_fraud"])
        )
    )

    connection.commit()

    print(
        "Transaction:", transaction["transaction_id"],
        "| Amount:", transaction["amount"],
        "| Risk Score:", risk_score,
        "| Risk:", risk_level,
        "| Stored in PostgreSQL"
    )