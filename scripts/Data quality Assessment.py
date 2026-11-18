#!/usr/bin/env python3
"""Print a quality summary of the three raw datasets. Read-only.

Run from the project folder, or set PROJECT_ROOT.
"""
import os
from pathlib import Path
import pandas as pd

START, END = "2023-01-01", "2024-12-31"
INJURY_RANK = {
    "NO INDICATION OF INJURY": 0, "REPORTED, NOT EVIDENT": 1,
    "NONINCAPACITATING INJURY": 2, "INCAPACITATING INJURY": 3, "FATAL": 4,
}
INJURY_LABEL = {}
for name, n in INJURY_RANK.items():
    INJURY_LABEL[n] = name
ID_COLS = {"crash_record_id", "person_id", "station", "vehicle_id",
           "zipcode", "ems_run_no", "idot_control_no"}


def find_root():
    if os.environ.get("PROJECT_ROOT"):
        return Path(os.environ["PROJECT_ROOT"]).resolve()
    here = Path(__file__).resolve().parent
    for path in [Path.cwd(), here, *here.parents]:
        if (path / "data" / "raw" / "crashes_2023_2024.csv").exists():
            return path
    raise SystemExit("Could not find data/raw/crashes_2023_2024.csv. "
                     "Run this from the project folder or set PROJECT_ROOT.")


def read_csv(path):
    # Keep ID columns as text so long IDs are not changed.
    dtypes = {}
    for c in pd.read_csv(path, nrows=0).columns:
        if c.lower() in ID_COLS:
            dtypes[c] = "string"
    # These read options must stay so missing values match the original script.
    return pd.read_csv(path, dtype=dtypes, dtype_backend="numpy_nullable",
                       low_memory=False, keep_default_na=False, na_values=[""])


def pct(n, d):
    return f"{n / d * 100:.2f}%" if d else "n/a"


def show_missing(df, title):
    print(f"\n{title}")
    print(f"{'Field':<36} {'Missing':>10} {'Share':>10}")
    for col, n in df.isna().sum().items():
        if n:
            print(f"{col:<36} {n:10,} {pct(n, len(df)):>10}")


raw = find_root() / "data" / "raw"
crashes = read_csv(raw / "crashes_2023_2024.csv")
people = read_csv(raw / "people_2023_2024.csv")
noaa = read_csv(raw / "noaa_usw00094846.csv")

print("=== Crashes ===")
print(f"Rows: {len(crashes):,}  Columns: {crashes.shape[1]}")
print(f"Unique crash_record_id: {crashes['crash_record_id'].nunique():,}")
print(f"Missing IDs: {int(crashes['crash_record_id'].isna().sum())}")
print(f"Exact duplicate rows: {int(crashes.duplicated().sum())}")
crash_date = pd.to_datetime(crashes["crash_date"], format="mixed", errors="coerce")
notify = pd.to_datetime(crashes["date_police_notified"], format="mixed", errors="coerce")
lag_hours = (notify - crash_date).dt.total_seconds() / 3600
print(f"crash_date range: {crash_date.min()} to {crash_date.max()}")
print(f"Dates outside 2023-2024: {int(((crash_date < START) | (crash_date > END + ' 23:59:59')).sum())}")
print(f"Police notified more than 1 day later: {int((lag_hours > 24).sum()):,}")
print(f"Police notified more than 30 days later: {int((lag_hours > 720).sum()):,}")
print(f"Police notification in 2025 or later: {int((notify >= '2025-01-01').sum()):,}")
lat = pd.to_numeric(crashes["latitude"], errors="coerce")
lon = pd.to_numeric(crashes["longitude"], errors="coerce")
print(f"Missing latitude/longitude: {int(crashes['latitude'].isna().sum()):,}")
print(f"Coordinates at 0,0: {int(((lat == 0) & (lon == 0)).sum()):,}")
print(f"Missing injury totals: {int(crashes['injuries_total'].isna().sum()):,}")
print(f"Missing most severe injury: {int(crashes['most_severe_injury'].isna().sum()):,}")
for col in ["weather_condition", "lighting_condition", "roadway_surface_cond"]:
    n = int((crashes[col] == "UNKNOWN").sum())
    print(f"{col} = UNKNOWN: {n:,} ({pct(n, len(crashes))})")
show_missing(crashes, "Crashes fields with missing values")

print("\n=== People ===")
print(f"Rows: {len(people):,}  Columns: {people.shape[1]}")
print(f"Unique person_id: {people['person_id'].nunique():,}")
print(f"Exact duplicate rows: {int(people.duplicated().sum())}")
age = pd.to_numeric(people["age"], errors="coerce")
n_missing_age = int(people["age"].isna().sum())
print(f"Missing age: {n_missing_age:,} ({pct(n_missing_age, len(people))})")
print(f"Age below 0: {int((age < 0).sum())}  (values: {age[age < 0].tolist()})")
print(f"Age above 110: {int((age > 110).sum())}")
print(f"Age exactly 110: {int((age == 110).sum())}")
age0 = people.loc[(age == 0).fillna(False), "person_type"].value_counts()
print(f"Age 0 by person type:\n{age0.to_string()}")
print(f"Missing injury_classification: {int(people['injury_classification'].isna().sum())}")
print("injury_classification counts:")
print(people["injury_classification"].value_counts(dropna=False).to_string())
show_missing(people, "People fields with missing values")

print("\n=== NOAA (station USW00094846, O'Hare) ===")
dates = pd.to_datetime(noaa["DATE"], format="mixed", errors="coerce")
in_window = dates.between(START, END)
calendar = pd.date_range(START, END, freq="D").strftime("%Y-%m-%d")
observed = set(dates.loc[in_window].dt.strftime("%Y-%m-%d"))
print(f"Raw rows: {len(noaa):,}  Date range: {dates.min().date()} to {dates.max().date()}")
print(f"Rows in 2023-2024: {int(in_window.sum()):,}  (before: {int((dates < START).sum()):,}; after: {int((dates > END).sum()):,})")
print(f"Study days covered: {len(observed)} / {len(calendar)}  Missing days: {len(set(calendar) - observed)}")
print(f"Duplicate station-date rows: {int(noaa.duplicated(['STATION', 'DATE']).sum())}")
weather = noaa.loc[in_window].copy()
for col in ["PRCP", "TMAX", "TMIN", "SNOW", "SNWD"]:
    num = pd.to_numeric(weather[col], errors="coerce")
    print(f"{col} in study window: missing {int(weather[col].isna().sum())}, min {num.min()}, max {num.max()}")
# NOAA marks a trace of precipitation with T in the first attribute field.
trace = weather["PRCP_ATTRIBUTES"].astype("string").str.split(",").str[0] == "T"
prcp = pd.to_numeric(weather["PRCP"], errors="coerce")
print(f"Days with PRCP > 0: {int((prcp > 0).sum())}")
print(f"Days with PRCP = 0: {int((prcp == 0).sum())}  (of these, trace flag: {int(((prcp == 0) & trace).sum())})")

print("\n=== Links between datasets ===")
people_ok = people["crash_record_id"].isin(crashes["crash_record_id"])
crash_ok = crashes["crash_record_id"].isin(people["crash_record_id"])
print(f"People that match a crash: {int(people_ok.sum()):,} / {len(people):,} ({pct(int(people_ok.sum()), len(people))})")
print(f"Crashes with at least one person: {int(crash_ok.sum()):,} / {len(crashes):,} ({pct(int(crash_ok.sum()), len(crashes))})")
print(f"Crashes with no People rows: {int((~crash_ok).sum()):,}")
by_id = crashes.set_index("crash_record_id")["crash_date"]
people_date = pd.to_datetime(people["crash_date"], format="mixed", errors="coerce")
from_id = pd.to_datetime(people["crash_record_id"].map(by_id), format="mixed", errors="coerce")
both_ok = people_date.notna() & from_id.notna()
ts_diff = both_ok & (people_date != from_id)
day_diff = both_ok & (people_date.dt.normalize() != from_id.dt.normalize())
print(f"Same crash, different timestamps: {int(ts_diff.sum())} people in {people.loc[ts_diff, 'crash_record_id'].nunique()} crashes")
print(f"Of those, different calendar days: {int(day_diff.sum())}")
crash_day = crash_date.dt.strftime("%Y-%m-%d")
noaa_days = set(dates.dt.strftime("%Y-%m-%d"))
print(f"Crashes whose date exists in NOAA: {int(crash_day.isin(noaa_days).sum()):,} / {len(crashes):,}")

# Compare crash injury totals with counts from the People file.
sev = people["injury_classification"].astype("string").str.strip().str.upper().map(INJURY_RANK)
work = pd.DataFrame({
    "crash_record_id": people["crash_record_id"],
    "injured": (sev > 0).fillna(False).astype("Int64"),
    "severity": sev,
})
g = work.groupby("crash_record_id", dropna=False).agg(
    person_count=("injured", "size"),
    injured_count=("injured", "sum"),
    max_severity=("severity", "max"),
)
g["people_most_severe"] = g["max_severity"].map(INJURY_LABEL)
cmp = crashes[["crash_record_id", "injuries_total", "most_severe_injury"]].merge(
    g.reset_index(), on="crash_record_id", how="left"
)
has_people = cmp["person_count"].notna()
can_compare = has_people & cmp["injuries_total"].notna()
totals_agree = (cmp["injuries_total"] == cmp["injured_count"]).fillna(False)
print("Injury totals that agree with the People file: "
      f"{int((can_compare & totals_agree).sum()):,} / {int(can_compare.sum()):,} "
      f"(disagreements: {int((can_compare & ~totals_agree).sum()):,})")
can_compare_sev = has_people & cmp["most_severe_injury"].notna() & cmp["people_most_severe"].notna()
sev_agree = (cmp["most_severe_injury"] == cmp["people_most_severe"]).fillna(False)
print("Most severe injury that agrees with the People file: "
      f"{int((can_compare_sev & sev_agree).sum()):,} / {int(can_compare_sev.sum()):,} "
      f"(disagreements: {int((can_compare_sev & ~sev_agree).sum()):,})")
