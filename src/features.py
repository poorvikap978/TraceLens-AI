
import pandas as pd


def create_features(df):
    """Create rolling and change-based features for CPU data."""
    result = df.copy()

    result["rolling_mean"] = (
        result["value"]
        .rolling(window=12, min_periods=12)
        .mean()
    )

    result["rolling_std"] = (
        result["value"]
        .rolling(window=12, min_periods=12)
        .std()
    )

    result["change"] = result["value"].diff()

    result = result.dropna().reset_index(drop=True)

    return result


if __name__ == "__main__":
    from pathlib import Path
    from preprocessing import load_cpu_data

    project_root = Path(__file__).resolve().parent.parent
    data_path = (
        project_root
        / "data"
        / "sample"
        / "ec2_cpu_utilization.csv"
    )

    df = load_cpu_data(data_path)
    featured_data = create_features(df)

    print("Features created successfully!")
    print("\nColumns:")
    print(featured_data.columns.tolist())

    print("\nFirst five feature rows:")
    print(featured_data.head())

    print("\nDataset shape:", featured_data.shape)
