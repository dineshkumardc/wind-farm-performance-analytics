# Wind Farm Performance Analytics — Interview Project

## Purpose
A simulated wind farm dataset for practicing Python, R, statistics, time-series analysis, SCADA concepts, and operational KPI reporting.

## Files
- `wind_turbine_scada.csv` — hourly readings for six fictional turbines over ten days, with a few missing readings and one duplicate key.
- `event_log.csv` — sample fault, curtailment, and planned-maintenance events.
- `wind_analysis.py` — Python analysis.
- `wind_analysis.R` — R analysis.

## Suggested Setup

**Python**
```bash
pip install pandas numpy matplotlib
python wind_analysis.py
```

**R**
```r
install.packages(c("dplyr", "ggplot2", "readr"))
```
Open `wind_analysis.R` in RStudio and run it from the project folder.

## Business Questions
1. Which turbines have the lowest average power output?
2. Which records have missing actual power?
3. Are there duplicate turbine/timestamp keys?
4. What do status and fault-code counts show?
5. How does actual power relate to wind speed?
6. What is the estimated gap between illustrative expected and actual output?
7. Why is the estimated gap not automatically a confirmed energy-loss figure?
8. What additional data would you request before attributing underperformance to a fault?

## Important Assumptions and Limitations
- One row represents a one-hour interval. For this exercise, interval energy in kWh is approximated as average power in kW × 1 hour.
- `expected_power_kw` is generated using a simplified illustrative curve, not a manufacturer's certified power curve.
- Missing readings are not automatically converted to zero.
- Time-based availability needs a defined denominator and event/exclusion rules; do not infer a contractual availability KPI from this dataset alone.
- Curtailment loss estimates require a defensible estimate of what the turbine could have generated absent curtailment.
- The positive expected-versus-actual gap is a screening measure only.

## Interview Project Explanation
"I built a simulated wind farm performance analysis using Python and R. I checked data completeness and duplicate turbine/timestamp keys, summarized power output by turbine, examined wind-speed-to-power relationships, and reviewed status and fault events. The analysis demonstrates how I would investigate potential underperformance while distinguishing data-quality issues and operational restrictions from confirmed equipment faults."

## Completed Analysis and Results

### Data Quality Checks
- Original dataset: 1,441 rows, including one duplicate turbine/timestamp key.
- Cleaned dataset: 1,440 rows.
- Turbines analysed: 6 fictional turbines.
- Missing actual power readings: 8.
- Duplicate turbine/timestamp keys after cleaning: 0.
- Missing actual power readings were retained as missing, not replaced with zero.

### Python KPI Results
- Actual energy on valid readings: 555,894.7 kWh.
- Expected energy on valid readings: 587,006.1 kWh.
- Estimated energy gap on valid readings: 31,111.4 kWh.
- Weighted gap on valid readings: 5.30%.

These are illustrative results from a synthetic dataset. Energy is approximated using hourly average power multiplied by one hour. The estimated gap is a screening metric, not a confirmed energy-loss measurement.

### Event Analysis
Four illustrative events were analysed:
- E001 and E002: unplanned fault events on turbine T02.
- E003: curtailment event on turbine T04.
- E004: planned maintenance event on turbine T05.

Power output before, during, and after each event was compared descriptively. These comparisons do not prove that an event caused a particular performance change.

### Project Outputs
- `wind_turbine_scada_clean.csv` — cleaned SCADA dataset.
- `scada_analysis_output.csv` — analysed SCADA data with gap fields.
- `turbine_kpi_summary.csv` — turbine-level KPI summary.
- `event_analysis_summary.csv` — event-level analysis summary.
- `hourly_power_trend.png` — hourly power trend chart.
- `wind_speed_vs_power.png` — wind speed versus power chart.
- `Wind_Farm_Performance.pbix` — Power BI dashboard.

### Tools Used
- Python: pandas, NumPy, Matplotlib.
- R: dplyr, ggplot2, readr.
- Power BI: KPI cards, turbine comparison charts, status analysis, and DAX measures.

### Limitations and Next Steps
- The dataset is simulated and does not contain real Nordex operational data.
- The expected-power calculation uses a simplified illustrative curve, not a certified turbine power curve.
- Missing readings require investigation before estimating their impact.
- A production analysis would require verified SCADA data, turbine specifications, operating conditions, alarm history, and an agreed energy-loss methodology.
