# Credixis — Real-Time Credit Card Fraud & Risk Intelligence Platform

> An end-to-end data engineering platform for credit card transaction processing, fraud-risk analysis, streaming, graph-based investigation, API development, workflow orchestration, and data visualization.

---

## 📌 Overview

**Credixis** is a data engineering project that demonstrates how raw credit card transaction data can be transformed into actionable fraud and risk intelligence through an end-to-end data pipeline.

https://github.com/user-attachments/assets/55348bb2-2c43-4e37-b2a3-6f2e4d5ca626

The platform combines:

* Python-based data ingestion
* Data quality validation
* PostgreSQL
* SQL feature engineering
* Apache Spark
* Apache Kafka
* Rule-based risk scoring
* Neo4j graph analytics
* FastAPI
* React
* Apache Airflow
* Docker

The overall workflow is:

```text
Raw Credit Card Data
        │
        ▼
Data Validation
        │
        ▼
PostgreSQL
        │
   ┌────┴────┐
   ▼         ▼
SQL       Spark
Features  Batch Processing
   │         │
   └────┬────┘
        ▼
   Risk Engine
        │
   ┌────┴────┐
   ▼         ▼
 Kafka      Neo4j
Streaming  Identity Graph
   │         │
   └────┬────┘
        ▼
     FastAPI
        │
        ▼
 React Dashboard

      Airflow
   Orchestration
```

---

# 🎯 Project Objectives

Credixis was built to demonstrate practical data engineering concepts involved in financial transaction processing.

The main objectives are:

1. Ingest a large transaction dataset.
2. Validate transaction data quality.
3. Store transactions in PostgreSQL.
4. Perform SQL-based feature engineering.
5. Process transaction data using Apache Spark.
6. Stream transactions using Apache Kafka.
7. Generate interpretable transaction risk scores.
8. Model customer and transaction relationships using Neo4j.
9. Provide fraud investigation APIs using FastAPI.
10. Build an interactive React dashboard.
11. Orchestrate the data pipeline using Apache Airflow.
12. Containerize infrastructure using Docker.

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │   Credit Card CSV    │
                         │     284,807 rows     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Python Data Loader  │
                         │  Data Validation     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ PostgreSQL(OLTP)     │
                         │ Transaction Storage  │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌───────────────────┐           ┌─────────────────────────┐
          │ SQL Feature       │           │ Apache Spark (OLAP)     │
          │ Engineering       │           │ Batch Processing        │
          └─────────┬─────────┘           └────────┬────────────────┘
                    │                              │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │     Risk Engine      │
                         │  Rule-Based Scoring  │
                         └──────────┬───────────┘
                                    │
                       ┌────────────┴────────────┐
                       │                         │
                       ▼                         ▼
              ┌─────────────────┐       ┌─────────────────┐
              │ Apache Kafka    │       │      Neo4j      │
              │ Transaction     │       │ Identity Graph  │
              │ Streaming       │       │ Investigation   │
              └────────┬────────┘       └────────┬────────┘
                       │                         │
                       ▼                         │
              ┌─────────────────┐                │
              │ Kafka Consumer  │                │
              │ Risk Processing │                │
              └────────┬────────┘                │
                       │                         │
                       └────────────┬────────────┘
                                    │
                                    ▼
                          ┌─────────────────────┐
                          │       FastAPI       │
                          │      REST API       │
                          └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │   React Dashboard   │
                          │ Risk & Investigation│
                          └─────────────────────┘

                         Apache Airflow
                         Orchestration
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Data ingestion, validation & risk processing |
| **SQL / PostgreSQL** | Data storage, analytics & feature engineering |
| **PySpark** | Batch processing & feature engineering |
| **Apache Kafka** | Real-time transaction streaming |
| **Apache Airflow** | Pipeline orchestration |
| **Neo4j / Cypher** | Identity graph & fraud investigation |
| **FastAPI** | REST APIs for risk & investigation |
| **React** | Fraud monitoring dashboard |
| **Docker** | Containerized infrastructure |

# 📊 Dataset

Credixis uses the **ULB Credit Card Fraud Detection dataset**.

## Dataset Statistics

| Metric                  |    Value |
| ----------------------- | -------: |
| Total transactions      |  284,807 |
| Normal transactions     |  284,315 |
| Fraudulent transactions |      492 |
| Fraud rate              | ~0.1727% |
| Original columns        |       31 |
| Features                |   V1–V28 |
| Target                  |    Class |

The target column is:

```text
Class = 0 → Normal transaction
Class = 1 → Fraudulent transaction
```

The original dataset contains:

```text
Time
V1 - V28
Amount
Class
```

### Important Dataset Note

The original dataset does **not** contain:

* Customer IDs
* Device IDs
* IP addresses
* Merchant IDs

For the Neo4j identity graph, these attributes are **synthetically generated** to demonstrate entity relationships and fraud investigation.

They are not original attributes from the ULB dataset.

---

# 🔍 Data Quality Validation

Before processing the dataset, Credixis performs basic data-quality checks.

The validation process checks:

* Number of rows
* Number of columns
* Missing values
* Duplicate rows
* Invalid transaction amounts
* Fraud transaction count
* Normal transaction count

Example validation result:

```text
========== DATA QUALITY ==========

Rows: 284807
Columns: 31
Missing values: 0
Duplicate rows: 1081
Invalid amounts: 0
Fraud transactions: 492
Normal transactions: 284315
```

---

# 🗄️ PostgreSQL

PostgreSQL is used as the primary relational storage layer.

The main transaction table contains:

```text
transaction_id
transaction_time
amount
v1 ... v28
is_fraud
created_at
```

The streaming risk results are stored separately with information such as:

```text
transaction_id
customer_id
device_id
ip_address
merchant_id
amount
risk_score
risk_level
is_fraud
processed_at
```

PostgreSQL is used for:

* Transaction storage
* SQL analytics
* Feature engineering
* Risk result persistence
* Dashboard metrics
* API queries

---

# 🧮 Feature Engineering

Credixis generates transaction-level risk features using SQL and Spark.

## Previous Transaction Amount

SQL `LAG()` is used to obtain the previous transaction amount:

```sql
LAG(amount) OVER (
    ORDER BY transaction_time, transaction_id
)
```

---

## Amount Change

```text
amount_change =
current_amount - previous_amount
```

---

## Transaction Velocity

The number of transactions within a rolling 60-second window is calculated:

```text
transactions_last_60_seconds
```

This provides a transaction-velocity signal.

---

## Amount Deviation

```text
amount_deviation =
transaction_amount - overall_average_amount
```

---

## Recent Transaction Average

The average transaction amount within the recent 60-second window:

```text
avg_amount_last_60_seconds
```

---

## Recent Amount Ratio

```text
recent_amount_ratio =
current_amount / recent_average_amount
```

This compares the current transaction against recent transaction behavior.

---

# ⚡ Apache Spark Batch Processing

Credixis uses **PySpark** for batch feature engineering.

The Spark pipeline:

1. Reads the transaction dataset.
2. Calculates the overall average transaction amount.
3. Creates amount deviation.
4. Creates a 60-second rolling window.
5. Calculates transaction velocity.
6. Calculates recent transaction average.
7. Calculates recent amount ratio.
8. Generates fraud statistics.

Example:

```text
Spark started successfully!

Dataset loaded!

Number of rows: 284807

Overall average amount:
88.34961925093077
```

Fraud statistics:

```text
Class 0
Transactions: 284315
Average amount: approximately 88.29

Class 1
Transactions: 492
Average amount: approximately 122.21
```

---

# 🚨 Risk Engine

Credixis currently uses an **interpretable rule-based risk engine**.

The risk score is generated using transaction-level signals.

| Condition                      | Score |
| ------------------------------ | ----: |
| Amount > 500                   |   +20 |
| 10+ transactions in 60 seconds |   +20 |
| Recent amount ratio >= 2       |   +20 |
| Amount deviation > 200         |   +15 |
| Fraud label = 1                |   +25 |

Risk levels:

```text
Score >= 70
    ↓
HIGH

Score >= 40
    ↓
MEDIUM

Score < 40
    ↓
LOW
```

Current batch risk distribution:

```text
LOW       249,387
MEDIUM     26,253
HIGH        9,167
```

### Important

The current risk engine is a **rule-based portfolio implementation**, not a production fraud detection model.

The demonstration also uses the dataset's `Class` value as one of the scoring signals.

In a production real-time system, the ground-truth fraud label would not be available when an incoming transaction is scored.

---

# 📨 Apache Kafka Streaming

Credixis demonstrates transaction streaming using Apache Kafka.

The streaming architecture is:

```text
Transaction
     │
     ▼
Kafka Producer
     │
     ▼
credit_transactions
     │
     ▼
Kafka Consumer
     │
     ▼
Risk Calculation
     │
     ▼
PostgreSQL
```

The producer sends information such as:

```text
transaction_id
time
amount
customer_id
device_id
ip_address
merchant_id
is_fraud
```

The consumer:

1. Receives the transaction.
2. Calculates a risk score.
3. Assigns a risk level.
4. Stores the result in PostgreSQL.
5. Prints the processed transaction.

Kafka topic:

```text
credit_transactions
```

---

# 🕸️ Neo4j Identity Graph

Fraud investigation often requires understanding relationships between entities.

Credixis uses Neo4j to model:

```text
Customer
Device
IP Address
Merchant
Transaction
```

The graph contains relationships such as:

```text
Customer ──USES_DEVICE──► Device

Customer ──USES_IP──────► IP

Customer ──TRANSACTS_WITH──► Merchant

Customer ──MAKES───────► Transaction

Transaction ──TRANSACTS_WITH──► Merchant
```

Example investigation:

```text
Customer A
    │
    │ uses
    ▼
Device X
    ▲
    │ uses
    │
Customer B
    │
    ▼
Fraudulent Transactions
```

This allows investigators to explore:

* Shared devices
* Shared IP addresses
* Connected customers
* Customer transactions
* Connected fraudulent transactions
* Customer-merchant relationships

---

# 🔎 Fraud Investigation API

The FastAPI backend exposes Neo4j investigation functionality through:

```text
GET /fraud-investigation/{customer_id}
```

The endpoint can return connected customers, shared devices, and fraud transaction information.

Example investigation flow:

```text
Customer
   │
   ▼
Shared Device
   │
   ▼
Other Customer
   │
   ▼
Fraudulent Transactions
```

---

# 🌐 FastAPI Backend

FastAPI provides the REST API for Credixis.

## Endpoints

| Endpoint                                   | Description                          |
| ------------------------------------------ | ------------------------------------ |
| `GET /`                                    | API health/basic information         |
| `GET /risk-results`                        | Retrieve processed risk results      |
| `GET /risk-results/high`                   | Retrieve high-risk results           |
| `GET /risk-results/{transaction_id}`       | Retrieve a transaction's risk result |
| `GET /customers/{customer_id}/connections` | Retrieve customer connections        |
| `GET /fraud-investigation/{customer_id}`   | Investigate customer relationships   |
| `GET /dashboard/metrics`                   | Retrieve dashboard metrics           |

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 📊 Dashboard Metrics

The dashboard API provides:

* Total transactions
* Fraud transactions
* Fraud rate
* Average transaction amount
* Processed risk distribution

Example:

```json
{
    "total_transactions": 284807,
    "fraud_transactions": 492,
    "fraud_rate_percent": 0.1727,
    "average_transaction_amount": 88.35,
    "processed_risk_distribution": {
        "LOW": 418,
        "MEDIUM": 8,
        "HIGH": 0
    }
}
```

The processed risk distribution represents records that have gone through the Kafka risk pipeline and does not represent risk classifications for all 284,807 transactions.

---

# 🖥️ React Dashboard

Credixis includes a React + Vite dashboard.

The dashboard contains the following sections:

### ◈ Overview

Provides high-level transaction and fraud metrics.

### ⌁ Transactions

Displays processed transaction and risk information.

### ⚠ Risk Monitor

Displays risk-scored transactions and high-risk activity.

### ◎ Investigations

Allows customer-level fraud investigation.

### ◇ Identity Graph

Displays customer relationship information obtained from the Neo4j investigation layer.

The frontend communicates with FastAPI through REST APIs.

---

# 🔄 Apache Airflow

Apache Airflow orchestrates the main batch pipeline.

The current DAG is:

```text
validate_transactions
        │
        ▼
load_transactions_to_db
        │
        ▼
calculate_risk
        │
        ▼
load_to_neo4j
```

## Pipeline Tasks

### 1. Validate Transactions

Loads the source dataset and performs data-quality checks.

### 2. Load Transactions to PostgreSQL

Loads the transaction dataset into PostgreSQL.

The current implementation uses a full-refresh strategy.

### 3. Calculate Risk

Runs the risk-scoring pipeline.

### 4. Load to Neo4j

Builds the Neo4j identity graph from the enriched transaction data.

---

# 🐳 Docker

Docker is used to run the major infrastructure services.

Current services include:

```text
Apache Airflow
PostgreSQL
Redis
Neo4j
Apache Kafka
Zookeeper
```

Check running containers:

```bash
docker ps
```

---

# 🗂️ Project Structure

```text
Credixis/
│
├── api/
│   └── main.py
│
├── airflow/
│   └── dags/
│       └── credixis_pipeline.py
│
├── data/
│   └── creditcard.csv
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── spark/
│   └── batch_processing.py
│
├── src/
│   ├── data_loader.py
│   ├── load_to_db.py
│   ├── risk_engine.py
│   └── neo4j_loader.py
│
├── docker-compose.yml
├── docker-compose.neo4j.yml
├── .env
└── README.md
```

---

# 🛠️ Technology Stack

## Programming Languages

* Python
* SQL
* JavaScript
* JSX

## Data Engineering

* Apache Spark
* Apache Kafka
* Apache Airflow
* PostgreSQL

## Graph Database

* Neo4j
* Cypher

## Backend

* FastAPI
* Uvicorn
* REST APIs

## Frontend

* React
* Vite
* Axios
* CSS

## Infrastructure

* Docker
* Docker Compose

## Python Libraries

* Pandas
* PySpark
* psycopg2
* python-dotenv
* kafka-python
* Neo4j Python Driver

---

# 🚀 Getting Started

## Prerequisites

Install:

* Python 3.10+
* Node.js
* npm
* Docker Desktop
* Git
* Java 17+

---

## 1. Clone the Repository

```bash
git clone https://github.com/janhavichauhan/Credixis.git
cd Credixis
```

---

## 2. Create a Python Virtual Environment

```bash
python -m venv venv
```

### Windows

```cmd
venv\Scripts\activate
```

---

## 3. Install Python Dependencies

```bash
pip install pandas
pip install psycopg2-binary
pip install python-dotenv
pip install fastapi
pip install uvicorn
pip install kafka-python
pip install neo4j
pip install pyspark
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_connection_string

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

Do not commit the real `.env` file.

Use `.env.example` for sharing placeholder configuration.

---

# 🐳 Start Docker Services

Start the main Docker services:

```bash
docker compose up -d
```

Start Neo4j if using its separate Compose file:

```bash
docker compose -f docker-compose.neo4j.yml up -d
```

Check services:

```bash
docker ps
```

---

# 🗄️ PostgreSQL

Run the database connection test:

```bash
python src/test_db.py
```

Expected:

```text
Connected to Credixis PostgreSQL!
```

---

# ⚡ Spark

Run batch processing:

```bash
python spark/batch_processing.py
```

---

# 🚨 Risk Engine

Run:

```bash
python src/risk_engine.py
```

---

# 🕸️ Neo4j

Run the Neo4j loader:

```bash
python src/neo4j_loader.py
```

Neo4j Browser:

```text
http://localhost:7474
```

---

# 📨 Kafka

Start the Kafka consumer first, then run the producer.

The Kafka topic is:

```text
credit_transactions
```

Transactions are consumed, risk-scored, and stored in PostgreSQL.

---

# 🌐 FastAPI

Run:

```bash
uvicorn api.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🖥️ React

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite will provide the local frontend URL.

---

# 🔄 Airflow

Open the Airflow dashboard:

```text
http://localhost:8080
```

The main DAG:

```text
credixis_pipeline
```

Pipeline:

```text
Validate
   ↓
PostgreSQL
   ↓
Risk Engine
   ↓
Neo4j
```

---

# 📈 Current Results

Credixis successfully processes:

```text
284,807 total transactions
284,315 normal transactions
492 fraudulent transactions
```

Synthetic identity enrichment currently contains:

```text
5,000 customers
8,000 devices
10,000 IP addresses
1,000 merchants
```

The Neo4j graph models relationships between these entities and their transactions.

---

# 🧪 Data Engineering Concepts Demonstrated

Credixis demonstrates:

* Data ingestion
* Data validation
* ETL processing
* SQL analytics
* SQL window functions
* Batch processing
* Apache Spark
* Apache Kafka
* Streaming pipelines
* Feature engineering
* Rule-based risk scoring
* PostgreSQL
* Graph databases
* Neo4j
* Cypher
* Fraud investigation
* REST APIs
* FastAPI
* React
* Apache Airflow
* Workflow orchestration
* Docker
* Containerized infrastructure

---

# ⚠️ Project Limitations

Credixis is an educational and portfolio project and is not intended for production financial fraud detection.

## Synthetic Identity Data

The original dataset does not contain customer, device, IP, or merchant relationships.

These attributes are synthetically generated for the graph demonstration.

## Rule-Based Risk Scoring

The current risk engine uses manually defined rules instead of a trained machine-learning model.

## Fraud Label

The current demonstration uses the original fraud label as one of the risk-scoring signals.

A production system would not have the ground-truth fraud label at the time an incoming transaction is scored.

## Full-Refresh Loading

The current PostgreSQL loader uses a full-refresh strategy.

A production implementation could use incremental ingestion, CDC, upserts, and watermarks.

## Kafka Processing

The current Kafka implementation demonstrates streaming and risk processing.

Production improvements could include idempotent processing, exactly-once semantics, schema management, retries, dead-letter queues, and monitoring.

## Development Infrastructure

The Docker setup is designed for local development and portfolio demonstration rather than production deployment.

# 🎓 What This Project Demonstrates

Credixis demonstrates an end-to-end modern data engineering workflow:

```text
             RAW DATA
                │
                ▼
        DATA VALIDATION
                │
                ▼
         DATA INGESTION
                │
                ▼
        POSTGRESQL STORAGE
                │
        ┌───────┴───────┐
        ▼               ▼
   SQL FEATURES     SPARK BATCH
        │               │
        └───────┬───────┘
                ▼
           RISK ENGINE
                │
        ┌───────┴───────┐
        ▼               ▼
      KAFKA            NEO4J
    STREAMING      IDENTITY GRAPH
        │               │
        └───────┬───────┘
                ▼
             FASTAPI
                │
                ▼
         REACT DASHBOARD

             AIRFLOW
          ORCHESTRATION
```

The project brings together **batch processing, streaming, relational analytics, graph investigation, workflow orchestration, APIs, and visualization** into one end-to-end data engineering platform.

---

# 👩‍💻 Author

## Janhavi Chauhan


### Areas of Interest

* Data Engineering
* Backend Development
* Distributed Systems
* Data Pipelines
* Cloud Computing
* Fraud & Risk Analytics
* Software Engineering

---
<img width="798" height="242" alt="Screenshot 2026-10-02 190027" src="https://github.com/user-attachments/assets/c99043a7-faf9-4b54-8507-6467e1379cfb" />

<img width="935" height="270" alt="Screenshot 2026-10-02 171100" src="https://github.com/user-attachments/assets/f0bd8411-57dd-4cd6-9540-0d7d22589e11" />

<img width="803" height="247" alt="Screenshot 2026-10-02 190042" src="https://github.com/user-attachments/assets/5dfb9e8c-13a4-4a37-80a2-b89f1aaf1886" />

<img width="804" height="278" alt="Screenshot 2026-10-02 192403" src="https://github.com/user-attachments/assets/3a9cff43-2cdc-4724-b162-863659323328" />

<img width="869" height="332" alt="Screenshot 2026-10-02 150902" src="https://github.com/user-attachments/assets/4ca9d1bb-3af6-4bd7-8600-133c6a169890" />

<img width="800" height="344" alt="Screenshot 2026-10-02 120806" src="https://github.com/user-attachments/assets/6b8c94a0-e9b0-4968-a555-f5c7f9e079d5" />

<img width="905" height="377" alt="Screenshot 2026-10-02 152246" src="https://github.com/user-attachments/assets/729365f9-fb92-4eba-a54a-2135aba62ed2" />

<img width="924" height="267" alt="image" src="https://github.com/user-attachments/assets/78b9a256-c755-4150-9ed6-f9047c68779b" />

<img width="959" height="418" alt="image" src="https://github.com/user-attachments/assets/ba809a19-1e53-4ab9-a3f6-813f4277bc26" />










