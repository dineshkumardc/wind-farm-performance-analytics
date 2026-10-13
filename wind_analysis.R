# Wind Farm Performance Analytics — R starter
# Dataset is simulated for learning/interview practice.
# Run from this folder in R or RStudio.
# Packages: dplyr, ggplot2, readr

library(dplyr)
library(ggplot2)
library(readr)

df <- read_csv("wind_turbine_scada.csv", show_col_types = FALSE) %>%
  mutate(timestamp = as.POSIXct(timestamp, tz = "UTC"))

# 1. Data quality
cat("Rows:", nrow(df), " Columns:", ncol(df), "\n")
print(colSums(is.na(df)))
print(df %>% count(turbine_id, timestamp) %>% filter(n > 1))

# After reviewing duplicates, keep one record per turbine and timestamp.
df <- df %>%
  arrange(timestamp, turbine_id) %>%
  distinct(turbine_id, timestamp, .keep_all = TRUE)

# 2. Summary metrics. Each record represents one hour in this simulated dataset.
df <- df %>%
  mutate(
    actual_energy_kwh = actual_power_kw,
    expected_energy_kwh = expected_power_kw,
    estimated_gap_kwh = pmax(expected_energy_kwh - actual_energy_kwh, 0)
  )

summary <- df %>%
  group_by(turbine_id) %>%
  summarise(
    avg_actual_power_kw = mean(actual_power_kw, na.rm = TRUE),
    total_actual_energy_kwh = sum(actual_energy_kwh, na.rm = TRUE),
    total_expected_energy_kwh = sum(expected_energy_kwh, na.rm = TRUE),
    estimated_gap_kwh = sum(estimated_gap_kwh, na.rm = TRUE),
    missing_actual_readings = sum(is.na(actual_power_kw)),
    .groups = "drop"
  ) %>%
  mutate(gap_pct_of_expected =
           100 * estimated_gap_kwh / total_expected_energy_kwh)

print(summary)

# 3. Wind speed vs actual power
ggplot(filter(df, !is.na(actual_power_kw)),
       aes(x = wind_speed_ms, y = actual_power_kw, color = turbine_id)) +
  geom_point(alpha = 0.6) +
  labs(title = "Wind speed vs actual power",
       x = "Wind speed (m/s)", y = "Actual power (kW)") +
  theme_minimal()

# 4. Status counts
print(df %>% count(status, sort = TRUE))

# Caution: expected power is simulated. The gap is only a screening metric,
# not a confirmed energy-loss estimate or a Nordex-specific power curve.
