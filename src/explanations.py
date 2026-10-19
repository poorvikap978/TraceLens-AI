
def explain_incident(incident):
    """Generate a descriptive summary of an incident."""
    start = incident["start_time"]
    end = incident["end_time"]
    count = int(incident["anomaly_count"])
    minimum = float(incident["min_cpu"])
    maximum = float(incident["max_cpu"])

    duration = (end - start).total_seconds() / 60

    if minimum < 40 and maximum > 60:
        pattern = (
            "Both low and high CPU readings were observed. "
            "Investigate whether a spike was followed by a "
            "change in operating behavior."
        )
    elif maximum > 60:
        pattern = (
            "A high CPU reading was observed. "
            "Check nearby measurements and system activity."
        )
    elif minimum < 38:
        pattern = (
            "Low CPU readings were observed. "
            "Check whether this reflects a workload change "
            "or an unexpected system state."
        )
    else:
        pattern = (
            "CPU measurements were flagged as unusual. "
            "Review the surrounding time-series data."
        )

    return {
        "incident_start": start,
        "incident_end": end,
        "duration_minutes": round(duration, 1),
        "anomaly_count": count,
        "min_cpu": round(minimum, 3),
        "max_cpu": round(maximum, 3),
        "explanation": pattern,
        "confidence_note": (
            "This is a data-based observation, not proof "
            "of the underlying cause."
        ),
    }
