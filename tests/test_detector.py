
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from detector import detect_anomalies


def test_detector_returns_flags_and_scores():
    data = pd.DataFrame({
        "timestamp": pd.date_range(
            "2024-01-01", periods=30, freq="5min"
        ),
        "value": [40.0] * 29 + [100.0],
        "rolling_mean": [40.0] * 30,
        "rolling_std": [1.0] * 30,
        "change": [0.0] * 29 + [60.0],
    })

    result = detect_anomalies(data, contamination=0.1)

    assert "anomaly" in result.columns
    assert "anomaly_score" in result.columns
    assert result["anomaly"].dtype == bool
    assert result["anomaly_score"].notna().all()
    assert result["anomaly"].any()
