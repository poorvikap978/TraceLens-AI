
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from incident_grouper import group_anomalies


def test_groups_nearby_anomalies_into_incidents():
    data = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2024-01-01 00:00:00",
            "2024-01-01 00:05:00",
            "2024-01-01 00:10:00",
            "2024-01-01 01:00:00",
        ]),
        "value": [50.0, 60.0, 55.0, 70.0],
        "anomaly": [True, True, True, True],
    })

    result = group_anomalies(data, gap_minutes=15)

    assert result["incident_id"].nunique() == 2

    first_incident = result[
        result["incident_id"] == 1
    ]
    second_incident = result[
        result["incident_id"] == 2
    ]

    assert len(first_incident) == 3
    assert len(second_incident) == 1


def test_returns_empty_result_when_no_anomalies():
    data = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2024-01-01 00:00:00",
        ]),
        "value": [40.0],
        "anomaly": [False],
    })

    result = group_anomalies(data)

    assert result.empty
    assert "incident_id" in result.columns
