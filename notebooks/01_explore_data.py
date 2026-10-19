from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt 

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "sample"
    / "ec2_cpu_utilization.csv"
)

df = pd.read_csv(DATA_PATH)

print("\n--- First five rows ---")
print(df.head())

print("\n--- Dataset shape ---")
print(df.shape)

print("\n--- Dataset information ---")
df.info()

print("\n--- Missing values ---")
print(df.isnull().sum())

print("\n--- Statistical summary ---")
print(df.describe())



# Convert timestamp strings into datetime objects
df["timestamp"] = pd.to_datetime(df["timestamp"])

print("\n--- Updated data types ---")
print(df.dtypes)

# Check the time range covered by the dataset
print("\n--- Time range ---")
print("Start:", df["timestamp"].min())
print("End:", df["timestamp"].max())

# Check the time difference between consecutive records
print("\n--- Sampling intervals ---")
print(df["timestamp"].diff().value_counts().head())

# Confirm chronological ordering
print("\n--- Chronological check ---")
print("Sorted:", df["timestamp"].is_monotonic_increasing)



# Plot CPU measurements over time
plt.figure(figsize=(14, 5))

plt.plot(
    df["timestamp"],
    df["value"],
    linewidth=1,
    label="CPU utilization"
)

plt.title("EC2 CPU Utilization Over Time")
plt.xlabel("Timestamp")
plt.ylabel("CPU utilization value")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()


# Check unusually high and low CPU measurements
mean_value = df["value"].mean()
std_value = df["value"].std()

upper_limit = mean_value + (3 * std_value)
lower_limit = mean_value - (3 * std_value)

unusual_values = df[
    (df["value"] > upper_limit) |
    (df["value"] < lower_limit)
]

print("\n--- Statistical anomaly check ---")
print(f"Mean: {mean_value:.3f}")
print(f"Standard deviation: {std_value:.3f}")
print(f"Lower limit: {lower_limit:.3f}")
print(f"Upper limit: {upper_limit:.3f}")
print(f"Unusual observations: {len(unusual_values)}")
print(unusual_values.head(10))