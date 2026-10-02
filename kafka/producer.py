import json
import time
import pandas as pd
from kafka import KafkaProducer

DATA_PATH = "data/enriched_transactions.csv"
KAFKA_TOPIC = "credit_transactions"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

df = pd.read_csv(DATA_PATH)

print("Starting Kafka producer...")
print("Total transactions:", len(df))

for _, row in df.head(100).iterrows():
    transaction = {
        "transaction_id": int(row.name),
        "time": float(row["Time"]),
        "amount": float(row["Amount"]),
        "customer_id": row["customer_id"],
        "device_id": row["device_id"],
        "ip_address": row["ip_address"],
        "merchant_id": row["merchant_id"],
        "is_fraud": int(row["Class"])
    }

    producer.send(KAFKA_TOPIC, transaction)
    print("Sent:", transaction)

    time.sleep(0.1)

producer.flush()
producer.close()

print("Kafka producer completed!")