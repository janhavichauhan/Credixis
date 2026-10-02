import pandas as pd

INPUT_PATH = "data/enriched_transactions.csv"
OUTPUT_PATH = "data/risk_scored_transactions.csv"

def calculate_risk(row):
    score = 0

    if row["Amount"] > 500:
        score += 20

    if row["transactions_last_60_seconds"] >= 10:
        score += 20

    if row["recent_amount_ratio"] >= 2:
        score += 20

    if row["amount_deviation"] > 200:
        score += 15

    if row["Class"] == 1:
        score += 25

    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return pd.Series([score, risk_level])

def main():
    print("Loading enriched transactions...")

    df = pd.read_csv(INPUT_PATH)

    print("Calculating risk scores...")

    df["transactions_last_60_seconds"] = df["Time"].apply(
        lambda x: ((df["Time"] >= x - 60) & (df["Time"] <= x)).sum()
    )

    overall_average = df["Amount"].mean()

    df["amount_deviation"] = df["Amount"] - overall_average

    df["avg_amount_last_60_seconds"] = df["Time"].apply(
        lambda x: df.loc[
            (df["Time"] >= x - 60) & (df["Time"] <= x),
            "Amount"
        ].mean()
    )

    df["recent_amount_ratio"] = (
        df["Amount"] / df["avg_amount_last_60_seconds"]
    ).round(2)

    df[["risk_score", "risk_level"]] = df.apply(
        calculate_risk,
        axis=1
    )

    df.to_csv(OUTPUT_PATH, index=False)

    print("Risk scoring completed!")
    print("Rows:", len(df))

    print("\nRisk distribution:")
    print(df["risk_level"].value_counts())

    print("\nSample risk results:")
    print(
        df[
            [
                "Time",
                "Amount",
                "Class",
                "transactions_last_60_seconds",
                "recent_amount_ratio",
                "risk_score",
                "risk_level"
            ]
        ].head(20)
    )

if __name__ == "__main__":
    main()