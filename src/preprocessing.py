
from pathlib import Path

import pandas as pd


def load_cpu_data(file_path):
    """Load and validate CPU utilization time-series data."""
    df = pd.read_csv(file_path)

    required_columns = {"timestamp", "value"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Dataset must contain 'timestamp' and 'value' columns."
        )

    df = df[["timestamp", "value"]].copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )
    df["value"] = pd.to_numeric(
        df["value"], errors="coerce"
    )

    df = df.dropna(subset=["timestamp", "value"])
    df = df.sort_values("timestamp")
    df = df.drop_duplicates(subset=["timestamp"])
    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid observations found in the dataset.")

    return df


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    data_path = (
        project_root
        / "data"
        / "sample"
        / "ec2_cpu_utilization.csv"
    )

    data = load_cpu_data(data_path)

    print("Data loaded successfully!")
    print("Rows and columns:", data.shape)
    print("\nFirst five rows:")
    print(data.head())
    print("\nMissing values:")
    print(data.isnull().sum())
    print("\nChronologically sorted:", 
          data["timestamp"].is_monotonic_increasing)
