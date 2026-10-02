from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, round
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("CredixisBatchProcessing") \
    .master("local[*]") \
    .getOrCreate()

print("Spark started successfully!")

df = spark.read.csv(
    "data/creditcard.csv",
    header=True,
    inferSchema=True
)

print("Dataset loaded!")
print("Number of rows:", df.count())

overall_average = df.select(
    avg("Amount").alias("average_amount")
).collect()[0]["average_amount"]

print("Overall average amount:", overall_average)

df = df.withColumn(
    "amount_deviation",
    col("Amount") - overall_average
)

rolling_window = Window \
    .orderBy("Time") \
    .rangeBetween(-60, 0)

df = df.withColumn(
    "transactions_last_60_seconds",
    count("*").over(rolling_window)
)

df = df.withColumn(
    "avg_amount_last_60_seconds",
    avg("Amount").over(rolling_window)
)

df = df.withColumn(
    "recent_amount_ratio",
    round(
        col("Amount") / col("avg_amount_last_60_seconds"),
        2
    )
)

print("Transaction features:")

df.select(
    "Time",
    "Amount",
    "Class",
    "amount_deviation",
    "transactions_last_60_seconds",
    "avg_amount_last_60_seconds",
    "recent_amount_ratio"
).show(20)

fraud_stats = df.groupBy("Class").agg(
    count("*").alias("transaction_count"),
    avg("Amount").alias("average_amount")
)

print("Fraud statistics:")
fraud_stats.show()

spark.stop()