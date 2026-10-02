import pandas as pd
import hashlib

INPUT_PATH = "data/creditcard.csv"
OUTPUT_PATH = "data/enriched_transactions.csv"

def generate_id(prefix, value):
    hashed = hashlib.md5(str(value).encode()).hexdigest()[:8]
    return f"{prefix}_{hashed}"

def enrich_data(df):
    df["customer_id"] = df.index.map(
        lambda x: generate_id("CUS", x % 5000)
    )

    df["device_id"] = df.index.map(
        lambda x: generate_id("DEV", x % 8000)
    )

    df["ip_address"] = df.index.map(
        lambda x: f"192.168.{(x // 256) % 256}.{x % 256}"
    )

    df["merchant_id"] = df.index.map(
        lambda x: generate_id("MER", x % 1000)
    )

    return df

def main():
    print("Loading transactions...")
    df = pd.read_csv(INPUT_PATH)

    print("Creating synthetic identity data...")
    df = enrich_data(df)

    df.to_csv(OUTPUT_PATH, index=False)

    print("Identity enrichment completed!")
    print("Rows:", len(df))

    print("\nUnique identities:")
    print("Customers:", df["customer_id"].nunique())
    print("Devices:", df["device_id"].nunique())
    print("IP addresses:", df["ip_address"].nunique())
    print("Merchants:", df["merchant_id"].nunique())

    print("\nSample enriched transactions:")
    print(
        df[
            [
                "Time",
                "Amount",
                "Class",
                "customer_id",
                "device_id",
                "ip_address",
                "merchant_id"
            ]
        ].head(10)
    )

if __name__ == "__main__":
    main()