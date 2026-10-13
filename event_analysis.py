
import pandas as pd

# Load cleaned SCADA readings and operational events
scada = pd.read_csv(
    "wind_turbine_scada_clean.csv",
    parse_dates=["timestamp"]
)
events = pd.read_csv(
    "event_log.csv",
    parse_dates=["start_time", "end_time"]
)

print("\nEVENT-LEVEL SCADA ANALYSIS")
print("=" * 70)

for _, event in events.iterrows():
    turbine = event["turbine_id"]
    start = event["start_time"]
    end = event["end_time"]

    turbine_data = scada[scada["turbine_id"] == turbine].copy()

    # Use a half-open interval: start inclusive, end exclusive
    during = turbine_data[
        (turbine_data["timestamp"] >= start) &
        (turbine_data["timestamp"] < end)
    ]

    before = turbine_data[
        (turbine_data["timestamp"] >= start - pd.Timedelta(hours=6)) &
        (turbine_data["timestamp"] < start)
    ]

    after = turbine_data[
        (turbine_data["timestamp"] >= end) &
        (turbine_data["timestamp"] < end + pd.Timedelta(hours=6))
    ]

    print(f"\nEvent: {event['event_id']} | Turbine: {turbine}")
    print(f"Type: {event['event_type']}")
    print(f"Window: {start} to {end}")
    print(f"SCADA rows during event: {len(during)}")

    for label, window in [
        ("Before (6h)", before),
        ("During event", during),
        ("After (6h)", after)
    ]:
        valid = window["actual_power_kw"].dropna()
        avg_power = round(valid.mean(), 2) if len(valid) else None

        print(
            f"{label}: rows={len(window)}, "
            f"valid_power={len(valid)}, "
            f"avg_actual_power_kw={avg_power}"
        )

    if not during.empty:
        print("Status during event:")
        print(during["status"].value_counts().to_dict())

print("\nNote: Window comparisons are descriptive, not proof of causation.")


# Export event analysis results to CSV
summary_rows = []

for _, event in events.iterrows():
    turbine = event["turbine_id"]
    start = event["start_time"]
    end = event["end_time"]

    turbine_data = scada[scada["turbine_id"] == turbine]

    during = turbine_data[
        (turbine_data["timestamp"] >= start) &
        (turbine_data["timestamp"] < end)
    ]

    valid = during["actual_power_kw"].dropna()

    summary_rows.append({
        "event_id": event["event_id"],
        "turbine_id": turbine,
        "event_type": event["event_type"],
        "start_time": start,
        "end_time": end,
        "scada_rows_during_event": len(during),
        "valid_power_readings": len(valid),
        "avg_actual_power_kw": round(valid.mean(), 2) if len(valid) else "",
        "status_counts": str(during["status"].value_counts().to_dict()),
        "interpretation_note": "Descriptive only; not proof of causation"
    })

pd.DataFrame(summary_rows).to_csv(
    "event_analysis_summary.csv",
    index=False
)

print("Saved event_analysis_summary.csv")
