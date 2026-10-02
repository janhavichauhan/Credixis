import pandas as pd


DATA_PATH = "data/creditcard.csv"


def load_data():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    print("Dataset loaded successfully!")
    return df

def validate_data(df):

    print("\n========== DATA QUALITY ==========")

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    missing = df.isnull().sum().sum()
    print("Missing values:", missing)

    duplicates = df.duplicated().sum()
    print("Duplicate rows:", duplicates)

    invalid_amounts = (df["Amount"] < 0).sum()
    print("Invalid amounts:", invalid_amounts)

    fraud = df["Class"].sum()
    print("Fraud transactions:", fraud)

    normal = len(df) - fraud
    print("Normal transactions:", normal)


def main():

    df = load_data()
    validate_data(df)

if __name__ == "__main__":
    main()