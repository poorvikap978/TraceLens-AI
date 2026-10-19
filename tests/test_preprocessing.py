
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from preprocessing import load_cpu_data


def test_load_cpu_data_cleans_and_sorts_data(tmp_path):
    sample = pd.DataFrame({
        "timestamp": [
            "2024-01-01 00:10:00",
            "2024-01-01 00:00:00",
            "2024-01-01 00:10:00",
            "invalid",
        ],
        "value": [12.0, 10.0, 12.0, 15.0],
    })

    file_path = tmp_path / "sample.csv"
    sample.to_csv(file_path, index=False)

    result = load_cpu_data(file_path)

    assert len(result) == 2
    assert result["timestamp"].is_monotonic_increasing
    assert result["timestamp"].is_unique
    assert result["value"].notna().all()
