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

print("Kafka consumer started...")
print("Waiting for transactions...")

for message in consumer:
    transaction = message.value

    print(
        "Received transaction:",
        transaction["transaction_id"],
        "| Amount:",
        transaction["amount"],
        "| Customer:",
        transaction["customer_id"],
        "| Device:",
        transaction["device_id"]
    )