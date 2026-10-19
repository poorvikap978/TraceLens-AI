
import pandas as pd


def group_anomalies(df, gap_minutes=15):
    """Group nearby anomalous observations into incidents."""
    anomalies = (
        df[df["anomaly"]]
        .sort_values("timestamp")
        .copy()
        .reset_index(drop=True)
    )

    if anomalies.empty:
        anomalies["incident_id"] = pd.Series(dtype=int)
        return anomalies

    time_gaps = anomalies["timestamp"].diff()

    # Start a new incident when consecutive anomalies
    # are more than gap_minutes apart.
    new_incident = (
        time_gaps.isna()
        | (time_gaps > pd.Timedelta(minutes=gap_minutes))
    )

    anomalies["incident_id"] = new_incident.cumsum().astype(int)

    return anomalies


if __name__ == "__main__":
    from pathlib import Path
    from preprocessing import load_cpu_data
    from features import create_features
    from detector import detect_anomalies
    from explanations import explain_incident
    project_root = Path(__file__).resolve().parent.parent
    data_path = (
        project_root
        / "data"
        / "sample"
        / "ec2_cpu_utilization.csv"
    )

    raw_data = load_cpu_data(data_path)
    featured_data = create_features(raw_data)
    results = detect_anomalies(featured_data)

    incidents = group_anomalies(results)

    print("Total anomalies:", len(incidents))
    print("Incidents identified:", incidents["incident_id"].nunique())

    if not incidents.empty:
        summary = incidents.groupby("incident_id").agg(
            start_time=("timestamp", "min"),
            end_time=("timestamp", "max"),
            anomaly_count=("timestamp", "count"),
            min_cpu=("value", "min"),
            max_cpu=("value", "max"),
        )

        print("\nIncident summary:")
        print(summary.to_string())

        print("\n--- Incident explanations ---")

        if not summary.empty:
            for incident_id, row in summary.iterrows():
                explanation = explain_incident(row)

            print(f"\nIncident {incident_id}")
            print("Explanation:", explanation["explanation"])
            print(
                "Duration (minutes):",
                explanation["duration_minutes"],
            )
            print(
                "Confidence note:",
                explanation["confidence_note"],
            )
            print("\nIncident explanations:")