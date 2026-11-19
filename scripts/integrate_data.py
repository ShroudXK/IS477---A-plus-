"""Integrate the cleaned Crashes, People, and NOAA weather tables.

Run after scripts/clean_data.py:
    python scripts/integrate_data.py

Joins:
    People -> Crashes on crash_record_id (many people to one crash)
    Crashes -> Weather on crash_day = date (many crashes to one day)

It also checks the cross-table problems from Yifei's quality assessment
(Section 4) with her exact rules, adds flags, and stops if any count changes.

Outputs (in data/integrated/):
    person_level.csv         one row per person
    crash_level.csv          one row per crash
    daily.csv                one row per day (2023-2024)
    cross_table_review.csv   crashes with a cross-table problem, for review
    integration_summary.json row counts, match rates, flag counts, SHA-256
"""
import hashlib
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DIR = PROJECT_ROOT / "data" / "clean"
OUT_DIR = PROJECT_ROOT / "data" / "integrated"

# Injury order used in Yifei's script (higher number = more severe).
INJURY_RANK = {
    "NO INDICATION OF INJURY": 0,
    "REPORTED, NOT EVIDENT": 1,
    "NONINCAPACITATING INJURY": 2,
    "INCAPACITATING INJURY": 3,
    "FATAL": 4,
}
RANK_TO_LABEL = {}
for label, rank in INJURY_RANK.items():
    RANK_TO_LABEL[rank] = label

# Counts measured in Yifei's quality assessment. The script stops if any differ.
EXPECTED = {
    "crashes": 222810,
    "people": 491892,
    "weather_days": 731,
    "crashes_with_people": 222301,
    "crashes_without_people": 509,
    "timestamp_mismatch_people": 49,
    "timestamp_mismatch_crashes": 25,
    "day_mismatch_people": 29,
    "injury_total_mismatch": 240,
    "severity_mismatch": 3,
    "severity_blank_with_people": 3,
    "crashes_with_unknown_injury": 76,
}

# Columns kept in the output tables.
CRASH_COLUMNS = [
    "crash_record_id", "crash_date", "crash_day", "crash_hour",
    "crash_day_of_week", "crash_month", "weather_condition",
    "lighting_condition", "roadway_surface_cond", "crash_type",
    "first_crash_type", "prim_contributory_cause", "posted_speed_limit",
    "num_units", "most_severe_injury", "injuries_total", "injuries_fatal",
    "injuries_incapacitating", "injuries_non_incapacitating",
    "injuries_reported_not_evident", "injuries_no_indication",
    "injuries_unknown", "latitude", "longitude", "invalid_coordinates",
    "missing_coordinates", "injury_total_missing", "severity_missing",
]
PEOPLE_COLUMNS = [
    "person_id", "crash_record_id", "vehicle_id", "person_type", "crash_date",
    "sex", "age", "age_group", "invalid_age", "safety_equipment",
    "airbag_deployed", "injury_classification", "injured",
]
WEATHER_COLUMNS = [
    "date", "prcp_mm", "prcp_trace", "wet_day", "tmax_c", "tmin_c",
    "snow_mm", "snwd_mm",
]
COUNT_COLUMNS = [
    "injuries_total", "injuries_fatal", "injuries_incapacitating",
    "injuries_non_incapacitating", "injuries_reported_not_evident",
    "injuries_no_indication", "injuries_unknown", "crash_hour",
    "crash_day_of_week", "crash_month", "posted_speed_limit", "num_units",
]


def check(condition, message):
    """Stop the workflow with a clear message if a check fails."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")
    print(f"  ok: {message}")


def sha256(path):
    hash_value = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()


def read_clean(name, columns):
    path = CLEAN_DIR / name
    if not path.is_file():
        raise SystemExit(
            f"Missing {path}. Run 'python scripts/clean_data.py' first "
            "(or 'python scripts/run_all.py' for the whole workflow)."
        )
    # Same reading rule as cleaning: only empty cells are missing, IDs are text.
    return pd.read_csv(
        path, usecols=columns, low_memory=False,
        keep_default_na=False, na_values=[""],
        dtype={"crash_record_id": "string", "person_id": "string",
               "vehicle_id": "string"},
    )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- 1. Read the cleaned tables ----
    print("Reading cleaned tables ...")
    crashes = read_clean("crashes_clean.csv", CRASH_COLUMNS)
    people = read_clean("people_clean.csv", PEOPLE_COLUMNS)
    weather = read_clean("weather_clean.csv", WEATHER_COLUMNS)
    for name in COUNT_COLUMNS:
        crashes[name] = crashes[name].astype("Int64")
    people["age"] = people["age"].astype("Int64")
    people["injured"] = people["injured"].astype("Int64")
    # Keep the People file's own timestamp under a clear name.
    people = people.rename(columns={"crash_date": "person_crash_date"})

    print("Basic checks:")
    check(len(crashes) == EXPECTED["crashes"], f"{len(crashes):,} crashes")
    check(len(people) == EXPECTED["people"], f"{len(people):,} people")
    check(len(weather) == EXPECTED["weather_days"], f"{len(weather)} weather days")
    check(crashes["crash_record_id"].is_unique, "crash_record_id is unique")
    check(people["person_id"].is_unique, "person_id is unique")
    check(weather["date"].is_unique, "weather date is unique")

    # ---- 2. Join keys ----
    people_match = people["crash_record_id"].isin(crashes["crash_record_id"])
    crash_has_people = crashes["crash_record_id"].isin(people["crash_record_id"])
    crash_has_weather = crashes["crash_day"].isin(weather["date"])
    print("Join key checks:")
    check(people_match.all(), "every person matches a crash")
    check(crash_has_weather.all(), "every crash day has an O'Hare weather row")
    check(int(crash_has_people.sum()) == EXPECTED["crashes_with_people"],
          f"{int(crash_has_people.sum()):,} crashes have people")
    check(int((~crash_has_people).sum()) == EXPECTED["crashes_without_people"],
          f"{int((~crash_has_people).sum())} crashes have no people")

    # ---- 3. X2: same crash, different timestamp (Yifei's rule) ----
    crash_time = crashes.set_index("crash_record_id")["crash_date"]
    official_time = pd.to_datetime(
        people["crash_record_id"].map(crash_time), format="mixed", errors="coerce")
    person_time = pd.to_datetime(
        people["person_crash_date"], format="mixed", errors="coerce")
    both_ok = official_time.notna() & person_time.notna()
    people["date_mismatch"] = both_ok & (person_time != official_time)
    people["day_mismatch"] = both_ok & (
        person_time.dt.normalize() != official_time.dt.normalize())

    # ---- 4. Summarise people per crash (X3, X4, X5) ----
    people["severity_rank"] = (
        people["injury_classification"].map(INJURY_RANK).astype("Int64"))
    # Jacob's injured flag must agree with the severity rank.
    print("Injury flag check:")
    known = people["severity_rank"].notna()
    check((people.loc[known, "injured"] == (people.loc[known, "severity_rank"] > 0)
           .astype("Int64")).all(), "injured flag agrees with injury classification")
    people["injured_or_unknown_as_0"] = (people["severity_rank"] > 0).fillna(False).astype(int)
    people["injury_known"] = known.astype(int)
    people["injured_known"] = (people["injured"] == 1).fillna(False).astype(int)
    people["injury_unknown"] = (~known).astype(int)

    per_crash = people.groupby("crash_record_id").agg(
        person_count=("person_id", "size"),
        injured_people=("injured_known", "sum"),
        known_injury_people=("injury_known", "sum"),
        unknown_injury_people=("injury_unknown", "sum"),
        yifei_injured_count=("injured_or_unknown_as_0", "sum"),
        max_rank=("severity_rank", "max"),
        date_mismatch=("date_mismatch", "any"),
        day_mismatch=("day_mismatch", "any"),
    ).reset_index()
    per_crash["people_most_severe"] = per_crash["max_rank"].map(RANK_TO_LABEL)

    # ---- 5. Crash level table: crashes + people summary + weather ----
    crash_level = crashes.merge(per_crash, on="crash_record_id",
                                how="left", validate="one_to_one")
    crash_level = crash_level.merge(weather, left_on="crash_day", right_on="date",
                                    how="left", validate="many_to_one")
    crash_level = crash_level.drop(columns=["date"])

    has_people = crash_level["person_count"].notna()
    crash_level["has_people"] = has_people
    for name in ["person_count", "injured_people", "known_injury_people",
                 "unknown_injury_people"]:
        # Crashes with no people keep these as missing (unknown), not zero.
        crash_level[name] = crash_level[name].astype("Int64")
    crash_level["date_mismatch"] = crash_level["date_mismatch"].fillna(False).astype(bool)
    crash_level["day_mismatch"] = crash_level["day_mismatch"].fillna(False).astype(bool)

    # X3: crash injuries_total vs injured people count (Yifei's rule:
    # unknown injuries are counted as not injured in this comparison).
    can_compare = has_people & crash_level["injuries_total"].notna()
    totals_agree = (crash_level["injuries_total"] == crash_level["yifei_injured_count"]).fillna(False)
    crash_level["injury_total_mismatch"] = can_compare & ~totals_agree

    # X4: crash most_severe_injury vs most severe person in the crash.
    can_compare_sev = (has_people & crash_level["most_severe_injury"].notna()
                       & crash_level["people_most_severe"].notna())
    sev_agree = (crash_level["most_severe_injury"] == crash_level["people_most_severe"]).fillna(False)
    crash_level["severity_mismatch"] = can_compare_sev & ~sev_agree
    crash_level["severity_blank_with_people"] = has_people & crash_level["most_severe_injury"].isna()

    # X5: crash has at least one person with unknown injury.
    crash_level["has_unknown_injury"] = (crash_level["unknown_injury_people"] > 0).fillna(False).astype(bool)

    crash_level = crash_level.drop(columns=["max_rank", "yifei_injured_count"])

    print("Cross-table checks (Yifei Section 4):")
    n_people_ts = int(people["date_mismatch"].sum())
    n_crash_ts = int(crash_level["date_mismatch"].sum())
    n_people_day = int(people["day_mismatch"].sum())
    check(n_people_ts == EXPECTED["timestamp_mismatch_people"]
          and n_crash_ts == EXPECTED["timestamp_mismatch_crashes"],
          f"X2 timestamp mismatch: {n_people_ts} people in {n_crash_ts} crashes")
    check(n_people_day == EXPECTED["day_mismatch_people"],
          f"X2 different calendar day: {n_people_day} people")
    n_total = int(crash_level["injury_total_mismatch"].sum())
    check(n_total == EXPECTED["injury_total_mismatch"],
          f"X3 injury total mismatch: {n_total} of {int(can_compare.sum()):,} crashes")
    n_sev = int(crash_level["severity_mismatch"].sum())
    n_blank = int(crash_level["severity_blank_with_people"].sum())
    check(n_sev == EXPECTED["severity_mismatch"], f"X4 severity mismatch: {n_sev} crashes")
    check(n_blank == EXPECTED["severity_blank_with_people"],
          f"X4 blank severity but has people: {n_blank} crashes")
    n_unknown = int(crash_level["has_unknown_injury"].sum())
    check(n_unknown == EXPECTED["crashes_with_unknown_injury"],
          f"X5 crashes with unknown-injury people: {n_unknown}")

    # ---- 6. Person level table: people + official crash day + weather ----
    crash_info = crashes[["crash_record_id", "crash_date", "crash_day",
                          "weather_condition", "lighting_condition",
                          "roadway_surface_cond"]]
    person_level = people.merge(crash_info, on="crash_record_id",
                                how="left", validate="many_to_one")
    person_level = person_level.merge(weather, left_on="crash_day", right_on="date",
                                      how="left", validate="many_to_one")
    person_level = person_level.drop(columns=[
        "date", "severity_rank", "injured_or_unknown_as_0", "injury_known",
        "injured_known", "injury_unknown"])

    # ---- 7. Daily table: one row per day, crash counts + weather ----
    daily = crash_level.groupby("crash_day").agg(
        crash_count=("crash_record_id", "size"),
        crashes_without_people=("has_people", lambda s: int((~s).sum())),
        person_count=("person_count", "sum"),
        injured_people=("injured_people", "sum"),
        unknown_injury_people=("unknown_injury_people", "sum"),
    ).reset_index().rename(columns={"crash_day": "date"})
    # Start from the weather calendar so every day in 2023-2024 is kept.
    daily = weather.merge(daily, on="date", how="left", validate="one_to_one")
    for name in ["crash_count", "crashes_without_people", "person_count",
                 "injured_people", "unknown_injury_people"]:
        daily[name] = daily[name].fillna(0).astype(int)

    # ---- 8. Output checks ----
    print("Output checks:")
    check(len(crash_level) == EXPECTED["crashes"], f"crash_level keeps all {len(crash_level):,} crashes")
    check(len(person_level) == EXPECTED["people"], f"person_level keeps all {len(person_level):,} people")
    check(len(daily) == EXPECTED["weather_days"], f"daily has {len(daily)} days")
    check(crash_level["prcp_mm"].notna().all() and person_level["prcp_mm"].notna().all(),
          "every crash and person has weather")
    check(int(daily["crash_count"].sum()) == EXPECTED["crashes"], "daily crash counts add up to all crashes")
    check(int(daily["person_count"].sum()) == EXPECTED["people"], "daily person counts add up to all people")
    check((person_level["crash_day"] == person_level["crash_record_id"].map(
        crashes.set_index("crash_record_id")["crash_day"])).all(),
        "person weather uses the official Crashes date")

    # ---- 9. Review list of crashes with a cross-table problem ----
    flags = ["date_mismatch", "day_mismatch", "injury_total_mismatch",
             "severity_mismatch", "severity_blank_with_people", "has_unknown_injury"]
    any_flag = crash_level[flags].any(axis=1)
    person_dates = (people.loc[people["date_mismatch"]]
                    .groupby("crash_record_id")["person_crash_date"]
                    .agg(lambda s: "; ".join(sorted(set(s)))))
    review = crash_level.loc[any_flag, [
        "crash_record_id", "crash_date", "crash_day", "person_count",
        "injuries_total", "injured_people", "unknown_injury_people",
        "most_severe_injury", "people_most_severe"] + flags].copy()
    review.insert(3, "people_crash_dates_that_differ",
                  review["crash_record_id"].map(person_dates))
    review = review.sort_values("crash_record_id")

    # ---- 10. Save ----
    outputs = {
        "person_level.csv": person_level,
        "crash_level.csv": crash_level,
        "daily.csv": daily,
        "cross_table_review.csv": review,
    }
    output_sha = {}
    for name, table in outputs.items():
        path = OUT_DIR / name
        table.to_csv(path, index=False)
        output_sha[name] = sha256(path)
        print(f"Saved {path.relative_to(PROJECT_ROOT)} ({len(table):,} rows)")

    summary = {
        "inputs_sha256": {name: sha256(CLEAN_DIR / name) for name in
                          ["crashes_clean.csv", "people_clean.csv", "weather_clean.csv"]},
        "row_counts": {name: len(table) for name, table in outputs.items()},
        "match_rates": {
            "people_matched_to_crash": f"{int(people_match.sum())} / {len(people)}",
            "crashes_with_people": f"{int(crash_has_people.sum())} / {len(crashes)}",
            "crashes_matched_to_weather_day": f"{int(crash_has_weather.sum())} / {len(crashes)}",
            "weather_days_with_crashes": f"{int((daily['crash_count'] > 0).sum())} / {len(daily)}",
        },
        "cross_table_flags": {
            "crashes_without_people": int((~has_people).sum()),
            "timestamp_mismatch_people": n_people_ts,
            "timestamp_mismatch_crashes": n_crash_ts,
            "day_mismatch_people": n_people_day,
            "day_mismatch_crashes": int(crash_level["day_mismatch"].sum()),
            "injury_total_mismatch_crashes": n_total,
            "injury_total_compared_crashes": int(can_compare.sum()),
            "severity_mismatch_crashes": n_sev,
            "severity_blank_with_people_crashes": n_blank,
            "crashes_with_unknown_injury": n_unknown,
            "people_with_unknown_injury": int(person_level["injured"].isna().sum()),
            "crashes_in_review_list": len(review),
        },
        "outputs_sha256": output_sha,
    }
    with open(OUT_DIR / "integration_summary.json", "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)
    print(f"Summary saved to: data/integrated/integration_summary.json")


if __name__ == "__main__":
    main()
