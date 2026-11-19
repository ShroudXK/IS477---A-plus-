import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ID columns are read as text so 1668221 is not turned into 1668221.0.
ID_COLUMNS = ["crash_record_id", "person_id", "vehicle_id"]


def read_csv(path):
    header = pd.read_csv(path, nrows=0).columns
    id_types = {}
    for name in header:
        if name.strip().lower() in ID_COLUMNS:
            id_types[name] = "string"
    # Only empty cells count as missing. Text such as "NA" is kept as a value,
    # the same rule used in Yifei's quality assessment script.
    data = pd.read_csv(path, dtype=id_types, low_memory=False,
                       keep_default_na=False, na_values=[""])
    data.columns = data.columns.str.strip().str.lower()
    return data

def sha256(path):
    hash_value = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()

def clean_crashes(raw_folder, clean_folder):
    filename = "crashes_2023_2024.csv"
    df = read_csv(raw_folder / filename)
    rows_before = len(df)

    df["crash_record_id"] = (
        df["crash_record_id"].astype("string").str.strip()
    )
    crash_dates = pd.to_datetime(df["crash_date"], errors="coerce")
    df["crash_day"] = crash_dates.dt.strftime("%Y-%m-%d")

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    bad_location = (df["latitude"] == 0) & (df["longitude"] == 0)
    df["invalid_coordinates"] = bad_location
    df.loc[bad_location, ["latitude", "longitude", "location"]] = pd.NA
    df["missing_coordinates"] = (
        df["latitude"].isna() | df["longitude"].isna()
    )

    df["injury_total_missing"] = df["injuries_total"].isna()
    df["severity_missing"] = df["most_severe_injury"].isna()

    output = clean_folder / "crashes_clean.csv"
    df.to_csv(output, index=False)

    summary = {
        "rows_before": rows_before,
        "rows_after": len(df),
        "duplicate_crash_ids": int(df["crash_record_id"].duplicated().sum()),
        "invalid_zero_coordinates": int(bad_location.sum()),
        "missing_coordinates_after_cleaning": int(df["missing_coordinates"].sum()),
        "missing_injury_totals": int(df["injury_total_missing"].sum()),
        "missing_severity": int(df["severity_missing"].sum()),
        "date_parse_failures": int(crash_dates.isna().sum()),
    }
    del df
    return summary, output


def clean_people(raw_folder, clean_folder):
    filename = "people_2023_2024.csv"
    df = read_csv(raw_folder / filename)
    rows_before = len(df)

    for name in ["person_id", "crash_record_id"]:
        df[name] = df[name].astype("string").str.strip()

    df["person_type"] = df["person_type"].astype("string").str.strip().str.upper()
    df["injury_classification"] = (
        df["injury_classification"].astype("string").str.strip().str.upper()
    )

    person_dates = pd.to_datetime(df["crash_date"], errors="coerce")
    df["person_crash_day"] = person_dates.dt.strftime("%Y-%m-%d")

    # Ages are whole numbers; Int64 keeps them as 54 (not 54.0) and allows blanks.
    df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")
    df["age_original"] = df["age"].copy()
    negative_age = (df["age"] < 0).fillna(False)
    zero_non_passenger = ((df["age"] == 0) & df["person_type"].ne("PASSENGER").fillna(True)).fillna(False)
    bad_age = negative_age | zero_non_passenger
    df["invalid_age"] = bad_age
    df.loc[bad_age, "age"] = pd.NA

    df["age_group"] = pd.cut(
        df["age"].astype("float"),
        bins=[-1, 17, 24, 34, 44, 54, 64, float("inf")],
        labels=["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
    ).astype("string").fillna("Unknown")

    injury_codes = {
        "NO INDICATION OF INJURY": 0,
        "REPORTED, NOT EVIDENT": 1,
        "NONINCAPACITATING INJURY": 1,
        "INCAPACITATING INJURY": 1,
        "FATAL": 1,
    }
    df["injured"] = df["injury_classification"].map(injury_codes).astype("Int64")

    output = clean_folder / "people_clean.csv"
    df.to_csv(output, index=False)

    summary = {
        "rows_before": rows_before,
        "rows_after": len(df),
        "duplicate_person_ids": int(df["person_id"].duplicated().sum()),
        "negative_ages_corrected": int(negative_age.sum()),
        "zero_non_passenger_ages_corrected": int(zero_non_passenger.sum()),
        "total_ages_corrected": int(bad_age.sum()),
        "passengers_aged_zero_preserved": int(
            ((df["age"] == 0) & (df["person_type"] == "PASSENGER")).fillna(False).sum()
        ),
        "missing_ages_after_cleaning": int(df["age"].isna().sum()),
        "missing_injury_classification": int(df["injury_classification"].isna().sum()),
        "unknown_injury_flag": int(df["injured"].isna().sum()),
        "date_parse_failures": int(person_dates.isna().sum()),
    }
    del df
    return summary, output


def clean_weather(raw_folder, clean_folder):
    filename = "noaa_usw00094846.csv"
    df = read_csv(raw_folder / filename)
    rows_before = len(df)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.loc[
        df["date"].between("2023-01-01", "2024-12-31")
        & df["station"].astype("string").str.strip().eq("USW00094846")
    ].copy()

    df["prcp_mm"] = pd.to_numeric(df["prcp"], errors="coerce") / 10
    df["tmax_c"] = pd.to_numeric(df["tmax"], errors="coerce") / 10
    df["tmin_c"] = pd.to_numeric(df["tmin"], errors="coerce") / 10
    df["snow_mm"] = pd.to_numeric(df["snow"], errors="coerce")
    df["snwd_mm"] = pd.to_numeric(df["snwd"], errors="coerce")
    df["prcp_trace"] = (
        df["prcp_attributes"].astype("string").str.split(",").str[0]
        .str.strip().eq("T").fillna(False)
    )
    df["wet_day"] = (df["prcp_mm"] > 0).astype("Int64")
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    output = clean_folder / "weather_clean.csv"
    df.to_csv(output, index=False)

    summary = {
        "rows_before": rows_before,
        "rows_after": len(df),
        "rows_outside_study_period": rows_before - len(df),
        "duplicate_dates": int(df["date"].duplicated().sum()),
        "missing_precipitation": int(df["prcp_mm"].isna().sum()),
        "trace_precipitation_days": int(df["prcp_trace"].sum()),
        "days_with_measurable_precipitation": int(df["wet_day"].sum()),
        "days_with_zero_measured_precipitation": int((df["prcp_mm"] == 0).sum()),
    }
    del df
    return summary, output


def main():
    parser = argparse.ArgumentParser(description="Clean IS477 Chicago traffic project data")
    parser.add_argument("--raw-dir", type=Path, default=PROJECT_ROOT / "data" / "raw")
    parser.add_argument("--out-dir", type=Path, default=PROJECT_ROOT / "data" / "clean")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    names = ["crashes_2023_2024.csv", "people_2023_2024.csv", "noaa_usw00094846.csv"]
    for name in names:
        if not (args.raw_dir / name).is_file():
            raise FileNotFoundError(f"Missing {name} in {args.raw_dir}")

    summary = {
        "source": "Yifei Zhang's dataset quality assessment (2023-2024)",
        "input_sha256": {name: sha256(args.raw_dir / name) for name in names},
        "datasets": {},
    }

    for name, method in [
        ("crashes", clean_crashes),
        ("people", clean_people),
        ("weather", clean_weather),
    ]:
        stats, output = method(args.raw_dir, args.out_dir)
        stats["output_sha256"] = sha256(output)
        summary["datasets"][name] = stats
        print(f"{name}: {stats['rows_before']:,} -> {stats['rows_after']:,} rows")

    output = args.out_dir / "cleaning_summary.json"
    with open(output, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)
    print(f"Summary saved to: {output}")


if __name__ == "__main__":
    main()
