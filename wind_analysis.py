"""
Wind Farm Performance Analytics — Python starter
Dataset: simulated; for learning/interview practice only.
Run: python wind_analysis.py
Requires: pandas, numpy, matplotlib
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("wind_turbine_scada.csv", parse_dates=["timestamp"])

# 1. Data quality checks
print("Rows and columns:", df.shape)
print("\nMissing values:\n", df.isna().sum())
print("\nDuplicate turbine/timestamp keys:",
      df.duplicated(subset=["turbine_id", "timestamp"]).sum())

# Keep the first record for duplicate turbine/timestamp keys after reviewing the source.
df = df.drop_duplicates(subset=["turbine_id", "timestamp"], keep="first")


# 2. KPI summary: mean power is not energy.
# Assumption: each row represents a one-hour interval.
# Calculate gap KPIs only for rows with valid actual-power readings.

df["actual_energy_kwh"] = df["actual_power_kw"]
df["expected_energy_kwh"] = df["expected_power_kw"]

summary = df.groupby("turbine_id").agg(
    avg_actual_power_kw=("actual_power_kw", "mean"),
    total_actual_energy_kwh=("actual_energy_kwh", "sum"),
    total_expected_energy_kwh=("expected_energy_kwh", "sum"),
    missing_actual_readings=("actual_power_kw", lambda s: s.isna().sum()),
    records=("timestamp", "count")
)

# Use only rows where actual power is available for gap calculations.
valid_df = df.dropna(subset=["actual_power_kw"]).copy()

valid_df["estimated_gap_kwh"] = (
    valid_df["expected_energy_kwh"] - valid_df["actual_energy_kwh"]
).clip(lower=0)

valid_summary = valid_df.groupby("turbine_id").agg(
    expected_energy_valid_kwh=("expected_energy_kwh", "sum"),
    estimated_gap_kwh=("estimated_gap_kwh", "sum")
)

summary = summary.join(valid_summary)

summary["gap_pct_of_expected_valid"] = (
    summary["estimated_gap_kwh"]
    / summary["expected_energy_valid_kwh"] * 100
)

print("\nTurbine summary:\n", summary.round(2))

# 3. Event/status counts
print("\nStatus counts:\n", df["status"].value_counts(dropna=False))
print("\nFault-code counts:\n", df.loc[df["fault_code"].notna() & (df["fault_code"] != ""),
                                       "fault_code"].value_counts())

# 4. Wind speed vs power output scatterplot
plot_df = df.dropna(subset=["wind_speed_ms", "actual_power_kw"])
plt.figure()
for turbine_id, group in plot_df.groupby("turbine_id"):
    plt.scatter(group["wind_speed_ms"], group["actual_power_kw"], label=turbine_id, alpha=0.6)
plt.xlabel("Wind speed (m/s)")
plt.ylabel("Actual power (kW)")
plt.title("Wind speed vs actual power by turbine")
plt.legend()
plt.tight_layout()
plt.savefig("wind_speed_vs_power.png", dpi=150)
print("\nSaved chart: wind_speed_vs_power.png")

# 5. Hourly trends (mean power across turbines)
hourly = df.groupby("timestamp")["actual_power_kw"].mean()
plt.figure()
hourly.plot()
plt.xlabel("Timestamp")
plt.ylabel("Mean actual power (kW)")
plt.title("Wind farm mean power output over time")
plt.tight_layout()
plt.savefig("hourly_power_trend.png", dpi=150)
print("Saved chart: hourly_power_trend.png")

# Interpretation caution:
# expected_power_kw is an illustrative model, not a manufacturer's certified power curve.
# A positive expected-actual gap is a screening indicator, not a confirmed energy-loss figure.
