
import json
from pathlib import Path

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from src.preprocessing import load_cpu_data
from src.features import create_features
from src.detector import detect_anomalies


def load_reference_labels(data, labels_path):
    """Label observations that fall inside reference anomaly windows."""
    with open(labels_path, "r", encoding="utf-8") as file:
        reference = json.load(file)

    labels = [False] * len(data)

    for window in reference["reference_windows"]:
        start = __import__("pandas").Timestamp(window["start"])
        end = __import__("pandas").Timestamp(window["end"])

        inside_window = (
            (data["timestamp"] >= start)
            & (data["timestamp"] <= end)
        )

        for index in range(len(data)):
            if inside_window.iloc[index]:
                labels[index] = True

    return labels


def evaluate_model():
    project_root = Path(__file__).resolve().parent

    data_path = (
        project_root
        / "data"
        / "sample"
        / "ec2_cpu_utilization.csv"
    )

    labels_path = (
        project_root
        / "data"
        / "labels"
        / "nab_reference_windows.json"
    )

    raw_data = load_cpu_data(data_path)
    featured_data = create_features(raw_data)
    results = detect_anomalies(featured_data)

    y_true = load_reference_labels(results, labels_path)
    y_pred = results["anomaly"].tolist()

    precision = precision_score(
        y_true, y_pred, zero_division=0
    )
    recall = recall_score(
        y_true, y_pred, zero_division=0
    )
    f1 = f1_score(
        y_true, y_pred, zero_division=0
    )

    tn, fp, fn, tp = confusion_matrix(
        y_true, y_pred, labels=[False, True]
    ).ravel()

    print("TraceLens AI — Benchmark Window Evaluation")
    print("------------------------------------------")
    print("Observations evaluated:", len(results))
    print("Reference-positive observations:", sum(y_true))
    print("Predicted anomalies:", sum(y_pred))
    print()
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-score:  {f1:.4f}")
    print()
    print("Confusion matrix counts:")
    print("True positives:", tp)
    print("False positives:", fp)
    print("True negatives:", tn)
    print("False negatives:", fn)
    print()
    print(
        "Evaluation note: reference windows were converted "
        "to point-level labels. These metrics may differ from "
        "the official NAB scoring method."
    )


if __name__ == "__main__":
    evaluate_model()
