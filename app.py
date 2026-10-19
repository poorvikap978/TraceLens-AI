
from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Allow imports from the src folder
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from preprocessing import load_cpu_data
from features import create_features
from detector import detect_anomalies
from incident_grouper import group_anomalies
from explanations import explain_incident


st.set_page_config(
    page_title="TraceLens AI",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 TraceLens AI")
st.subheader("Anomaly Detection and Incident Analysis")

st.write(
    "Explore unusual CPU behavior, group anomalies into incidents, "
    "and review evidence-based explanations."
)

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "sample"
    / "ec2_cpu_utilization.csv"
)

@st.cache_data
def load_results():
    raw_data = load_cpu_data(DATA_PATH)
    featured_data = create_features(raw_data)
    detected_data = detect_anomalies(featured_data)
    incidents = group_anomalies(detected_data)

    return detected_data, incidents


try:
    results, incidents = load_results()

    total_observations = len(results)
    total_anomalies = int(results["anomaly"].sum())
    total_incidents = int(incidents["incident_id"].nunique())

    col1, col2, col3 = st.columns(3)

    col1.metric("Observations analyzed", total_observations)
    col2.metric("Anomalies detected", total_anomalies)
    col3.metric("Potential incidents", total_incidents)

    st.divider()

    st.header("CPU utilization over time")

    fig = px.line(
        results,
        x="timestamp",
        y="value",
        title="CPU Measurements and Detected Anomalies",
        labels={
            "timestamp": "Timestamp",
            "value": "CPU utilization",
        },
    )

    anomaly_points = results[results["anomaly"]]

    fig.add_scatter(
        x=anomaly_points["timestamp"],
        y=anomaly_points["value"],
        mode="markers",
        name="Detected anomalies",
        marker=dict(color="red", size=8),
    )

    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.header("Detected observations")

    st.dataframe(
        results[results["anomaly"]][
            ["timestamp", "value", "anomaly_score"]
        ].sort_values("anomaly_score", ascending=False),
        use_container_width=True,
    )


    st.divider()
    st.header("Incident investigation")

    if incidents.empty:
        st.info("No incidents detected.")
    else:
        incident_summary = (
            incidents.groupby("incident_id")
            .agg(
                start_time=("timestamp", "min"),
                end_time=("timestamp", "max"),
                anomaly_count=("timestamp", "count"),
                min_cpu=("value", "min"),
                max_cpu=("value", "max"),
            )
            .reset_index()
        )

        st.dataframe(
            incident_summary,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Evidence-based explanations")

        for _, incident in incident_summary.iterrows():
            explanation = explain_incident(incident)

            with st.expander(
                f"Incident {int(incident['incident_id'])}"
                f" — {int(incident['anomaly_count'])} anomalies"
            ):
                st.write(explanation["explanation"])
                st.write(
                    f"**Time range:** {incident['start_time']} "
                    f"to {incident['end_time']}"
                )
                st.write(
                    f"**CPU range:** {incident['min_cpu']:.3f} "
                    f"to {incident['max_cpu']:.3f}"
                )
                st.caption(explanation["confidence_note"])


except Exception as error:
    st.error(f"Unable to load the dashboard: {error}")
    st.exception(error)
