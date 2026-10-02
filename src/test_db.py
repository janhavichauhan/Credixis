import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


connection = psycopg2.connect(DATABASE_URL)

print("Connected to Credixis PostgreSQL!")

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM transactions;")

result = cursor.fetchone()

print("Transactions in database:", result[0])

cursor.close()
connection.close()