import json
from kafka import KafkaConsumer

KAFKA_TOPIC = "credit_transactions"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="credixis-risk-consumer",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

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

    print(
        "Transaction:", transaction["transaction_id"],
        "| Amount:", transaction["amount"],
        "| Customer:", transaction["customer_id"],
        "| Device:", transaction["device_id"],
        "| Risk Score:", risk_score,
        "| Risk:", risk_level
    )