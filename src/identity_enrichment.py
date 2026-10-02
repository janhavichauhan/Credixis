import pandas as pd
import hashlib
import random


INPUT_PATH = "data/creditcard.csv"
OUTPUT_PATH = "data/enriched_transactions.csv"


# Make results reproducible
random.seed(42)


def generate_id(prefix, value):
    hashed = hashlib.md5(str(value).encode()).hexdigest()[:8]
    return f"{prefix}_{hashed}"


def enrich_data(df):

    # ---------------------------------
    # 1. Create customers
    # ---------------------------------

    NUM_CUSTOMERS = 5000

    df["customer_number"] = [
        random.randint(0, NUM_CUSTOMERS - 1)
        for _ in range(len(df))
    ]

    df["customer_id"] = df["customer_number"].map(
        lambda x: generate_id("CUS", x)
    )


    # ---------------------------------
    # 2. Create devices
    # ---------------------------------

    NUM_DEVICES = 8000

    df["device_number"] = [
        random.randint(0, NUM_DEVICES - 1)
        for _ in range(len(df))
    ]

    df["device_id"] = df["device_number"].map(
        lambda x: generate_id("DEV", x)
    )


    # ---------------------------------
    # 3. Create IP addresses
    # ---------------------------------

    NUM_IPS = 10000

    df["ip_number"] = [
        random.randint(0, NUM_IPS - 1)
        for _ in range(len(df))
    ]

    df["ip_address"] = df["ip_number"].map(
        lambda x: f"192.168.{(x // 256) % 256}.{x % 256}"
    )


    # ---------------------------------
    # 4. Create merchants
    # ---------------------------------

    NUM_MERCHANTS = 1000

    df["merchant_number"] = [
        random.randint(0, NUM_MERCHANTS - 1)
        for _ in range(len(df))
    ]

    df["merchant_id"] = df["merchant_number"].map(
        lambda x: generate_id("MER", x)
    )


    # Remove helper columns

    df.drop(
        columns=[
            "customer_number",
            "device_number",
            "ip_number",
            "merchant_number"
        ],
        inplace=True
    )


    return df


def main():

    print("Loading transactions...")

    df = pd.read_csv(INPUT_PATH)

    print("Creating synthetic identity data...")

    df = enrich_data(df)

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("Identity enrichment completed!")

    print("Rows:", len(df))


    print("\nUnique identities:")

    print(
        "Customers:",
        df["customer_id"].nunique()
    )

    print(
        "Devices:",
        df["device_id"].nunique()
    )

    print(
        "IP addresses:",
        df["ip_address"].nunique()
    )

    print(
        "Merchants:",
        df["merchant_id"].nunique()
    )


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