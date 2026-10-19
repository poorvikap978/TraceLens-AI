
from sklearn.ensemble import IsolationForest


def detect_anomalies(df, contamination=0.01):
    """Detect unusual CPU behavior using Isolation Forest."""
    result = df.copy()

    feature_columns = [
        "value",
        "rolling_mean",
        "rolling_std",
        "change",
    ]

    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42,
    )

    model.fit(result[feature_columns])

    predictions = model.predict(result[feature_columns])

    # Isolation Forest returns -1 for anomalies and 1 for normal points.
    result["anomaly"] = predictions == -1

    # Lower scores indicate observations that look more unusual.
    result["anomaly_score"] = -model.decision_function(
        result[feature_columns]
    )

    return result


if __name__ == "__main__":
    from pathlib import Path
    from preprocessing import load_cpu_data
    from features import create_features

    project_root = Path(__file__).resolve().parent.parent
    data_path = (
        project_root
        / "data"
        / "sample"
        / "ec2_cpu_utilization.csv"
    )

    df = load_cpu_data(data_path)
    featured_data = create_features(df)
    results = detect_anomalies(featured_data)

    anomalies = results[results["anomaly"]]

    print("Anomaly detection completed!")
    print("Total observations:", len(results))
    print("Anomalies detected:", len(anomalies))
    anomaly_percentage = len(anomalies) / len(results) * 100

    print(f"Anomaly percentage: {anomaly_percentage:.2f}%")
    print(
        "Normal observations:",
        len(results) - len(anomalies),
    )

    print("\nTop 10 unusual observations:")
    print(
        anomalies.sort_values(
            "anomaly_score", ascending=False
        )[
            ["timestamp", "value", "anomaly_score"]
        ].head(10).to_string(index=False)
    )

    import matplotlib.pyplot as plt

    plt.figure(figsize=(14, 5))

    plt.plot(
        results["timestamp"],
        results["value"],
        label="CPU utilization",
        linewidth=1,
    )

    plt.scatter(
        anomalies["timestamp"],
        anomalies["value"],
        color="red",
        label="Detected anomalies",
        s=25,
        zorder=3,
    )

    plt.title("TraceLens AI: Detected CPU Anomalies")
    plt.xlabel("Timestamp")
    plt.ylabel("CPU utilization value")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

