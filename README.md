# TraceLens AI
### Time-Series Anomaly Detection and Evidence-Based Incident Analysis

TraceLens AI is a Python-based monitoring prototype that identifies unusual patterns in system metrics, groups nearby anomalies into potential incidents, and generates evidence-based summaries through an interactive dashboard.

## Problem Statement

Monitoring systems can produce many unusual metric readings. Investigating individual readings separately makes it harder to understand when unusual behavior occurred and which observations may belong to the same event.

TraceLens AI explores a workflow for detecting unusual CPU measurements and organizing them into incident timelines.

## Key Features

- **Data preprocessing:** Validates timestamps and numeric values, removes invalid records and duplicate timestamps, and sorts observations chronologically.
- **Feature engineering:** Calculates rolling averages, rolling standard deviations, and changes between consecutive measurements.
- **Anomaly detection:** Uses the Isolation Forest algorithm to flag unusual observations.
- **Incident grouping:** Groups nearby flagged observations based on a configurable time gap.
- **Evidence-based explanations:** Summarizes observed CPU patterns without claiming an unverified root cause.
- **Interactive dashboard:** Displays CPU measurements, anomaly markers, summary metrics, incident tables, and explanations.
- **Automated tests:** Tests core preprocessing, detection, and incident-grouping behavior.

## Technology Stack

- Python
- pandas and NumPy
- scikit-learn
- Plotly
- Streamlit
- pytest

## Dataset

The initial prototype uses the EC2 CPU utilization time series from the Numenta Anomaly Benchmark (NAB), under `data/sample/ec2_cpu_utilization.csv`.

The dataset is used to explore anomaly detection in historical CPU measurements.

## Project Structure

```text
TraceLens-AI/
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── preprocessing.py
│   ├── features.py
│   ├── detector.py
│   ├── incident_grouper.py
│   ├── explanations.py
│   └── reporting.py
├── data/
│   └── sample/
├── notebooks/
├── tests/
└── reports/
```

## Run Locally

1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment.
3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Launch the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

5. Open the local URL printed in the terminal.

## Run Tests

```bash
python -m pytest -v
```

## Current Limitations

- The anomaly detector uses a configurable contamination setting; flagged observations are not necessarily real incidents.
- Incident grouping uses temporal proximity and may combine different types of behavior.
- Explanations describe observed patterns and do not establish causation.
- The prototype currently focuses on one CPU time series and does not yet correlate independent metrics, application logs, or deployment events.

## Future Improvements

- Evaluate detection quality against labeled anomalies.
- Improve incident grouping and severity ranking.
- Add additional system metrics and log evidence.
- Compare Isolation Forest with statistical and alternative machine-learning baselines.
- Add reproducible experiments and deployment documentation.

## 🚀 Live Demo

**Try TraceLens AI:** [Launch the live application](https://tracelens-ai-lcqsjmy3ifxubsr3tbyqlx.streamlit.app/)

**Source Code:** [GitHub Repository](https://github.com/poorvikap978/TraceLens-AI)

TraceLens AI is a machine-learning application that detects anomalies in time-series CPU utilization data using Isolation Forest and generates rule-based incident explanations to help users investigate unusual behavior.  

## Disclaimer

TraceLens AI is an educational monitoring prototype. Its anomaly flags and explanations should be treated as investigation aids, not definitive diagnoses of system failures.
