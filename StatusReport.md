## Status Report

### Dataset Quality Assessment

**Section Prepared by:** Yifei Zhang\
**Role:** Assess the quality of the datasets\
**Data:** Chicago traffic crashes, people involved in those crashes, and daily weather at O'Hare, 2023–2024\

This report looks at how accurate, complete, timely, and consistent the three raw datasets are. The numbers were measured from the raw files, not guessed. Blank fields are treated as missing. Labels such as UNKNOWN or OTHER are kept as their own categories; they are not treated as blank.

The three files are:

- Crashes: `data/raw/crashes_2023_2024.csv` (222,810 rows, 49 columns)
- People: `data/raw/people_2023_2024.csv` (491,892 rows, 29 columns)
- Weather: `data/raw/noaa_usw00094846.csv` (29,249 raw rows; 731 of those days fall in 2023–2024)

A short script, [`Data quality Assessment.py`](scripts/Data%20quality%20Assessment.py), can be run to recompute these counts.

Every crash and every person has an ID, there are no duplicate records, and every crash date falls inside 2023–2024. Every person can be linked to a crash, and every crash day has a weather observation at O'Hare. The main problems are incomplete fields, a few impossible or unlikely values (especially ages and some map coordinates), disagreements between the files, and 509 crashes with no people listed. Blanks in special-case fields should not automatically be read as "no."

---

#### 1. Crashes dataset

All 222,810 crash IDs are present and unique, with no exact duplicate rows. Every `crash_date` falls between 2023-01-01 00:00:00 and 2024-12-31 23:47:00. Crash date, number of units, crash type, weather, lighting, and road surface have no blanks.

- **Injury totals missing (509 crashes, 0.23%):** Keep as missing. Do not replace with zero. These are the same 509 crashes with no People rows.
- **Most severe injury missing (512 crashes):** Keep as missing. 509 have no People rows; flag the other 3 for review. Do not guess.
- **Latitude and longitude missing (2,222 crashes, 1.00%):** Keep the crashes for dates and counts, but leave them off maps. Do not invent coordinates.
- **Coordinates recorded as 0,0 (17 crashes):** Not a real Chicago location, and outside a simple Chicago-area box. Treat as invalid, same as missing. Do not plot them or drop the crash.
- **Optional flags mostly blank (often 67%–99%), including hit-and-run, work zone, and lane count:** A blank does not clearly mean No, so do not fill it with "N." `lane_cnt` is 99.99% missing and should not be a main variable.
- **UNKNOWN categories:** weather 18,375 (8.25%), lighting 14,973 (6.72%), and road surface 29,176 (13.09%). Keep UNKNOWN as its own category. Do not fill it with CLEAR or DRY.
- **Late police notification:** 21,493 crashes more than one day later, 372 more than 30 days later, and 139 notifications in 2025 or later (as late as 2025-12-29). Use the crash date, not the notification date. Optionally flag late reports. No notification is earlier than the crash itself.

---

#### 2. People dataset

All 491,892 person IDs are present and unique, with no exact duplicate rows and no repeated person-and-crash pairs. Every person has a `crash_date` from 2023-01-01 through 2024-12-31, and every person links to a crash (100% match).

Age is missing for 143,698 people (29.21%). Among filled-in ages, 1 person has age **-59** (impossible), 0 are older than 110, and 1 is age 110. 3,074 people are listed as age 0: this can be a real infant passenger (1,109 rows), but not for other roles — 1,896 drivers, 41 pedestrians, 25 bicyclists, and 3 people in non-motor vehicles (1,965 in total).

- **Missing age (143,698 people, 29.21%):** Do not fill in an average age. Use an "unknown" age group in summaries.
- **Age is -59 (1 person):** Set this age to missing. Keep the person.
- **Age is 0 for non-passengers (1,965 people):** Set these ages to missing. Keep the 1,109 passengers with age 0.
- **Injury classification missing (101 people, 0.02%):** Do not recode as "no injury." Keep it missing, and keep the injured flag missing too.
- **cell_phone_use almost entirely blank (491,890 people):** Do not use this field, and do not treat blank as "no phone use."

---

#### 3. NOAA weather dataset (O'Hare, station USW00094846)

The raw file has 29,249 rows, from 1946-10-09 through 2026-11-10. For 2023–2024, all 731 days are present (including 2024-02-29), with no missing dates, no repeated station-date rows, and no missing PRCP, TMAX, TMIN, SNOW, or SNWD values. No day has a high temperature below the low temperature, and there are no negative precipitation or snow values.

The CSV headers do not state units. NOAA's GHCN-Daily documentation says PRCP is in tenths of a millimeter, TMAX and TMIN are in tenths of a degree Celsius, and SNOW and SNWD are already in millimeters. In 2023–2024 there are 260 days with precipitation above zero and 471 days with numeric PRCP of zero. 79 of those "zero" days have a trace flag (`T` in the PRCP attributes).

- **Many years outside 2023–2024 (27,839 days before; 679 after):** Filter the weather table to 2023–2024 only. Leave the raw file unchanged.
- **Units are not written in the CSV header:** Convert PRCP, TMAX, and TMIN by dividing by 10 (to mm and °C). Leave SNOW and SNWD as millimeters.
- **Trace precipitation recorded as PRCP = 0 (79 days):** Add a `prcp_trace` flag. Do not change the numeric PRCP value. If a "wet day" is PRCP > 0, say clearly that trace days are counted as dry.
- **Weather is from one airport station (O'Hare):** Use it as a city-wide daily summary, not the exact condition at the crash time or street.

---

#### 4. Problems that appear when the files are compared

Every person matches a crash (491,892 / 491,892), and every crash date has a weather day at O'Hare (222,810 / 222,810). Handle the issues below with flags and careful rules, not by deleting rows.

- **A crash has no people listed (509 crashes, 0.23%):** Keep these crashes in crash counts and daily totals. Leave injury outcome unknown, not zero.
- **Different times for the same crash (49 people in 25 crashes; 29 also differ by calendar day):** Keep both times. Use the Crashes date as the official crash day when joining to weather. Add a mismatch flag. Do not overwrite either timestamp.
- **Crash injury total does not match a count of injured people (240 of 222,301 crashes that have people):** Keep both numbers and list the disagreements for review. Do not auto-correct one file with the other.
- **Crash "most severe injury" does not match the people in that crash (3 disagreements, plus 3 crashes that have people but a blank severity):** Keep the original values, flag them, and do not invent a correction.
- **Some crashes have people whose injury is unknown (76 crashes):** Only count known injuries. Do not treat an unknown injury as "not injured."

---

#### 5. Short recommendations for the next steps

Do not drop rows because a field is missing or a value looks wrong, and do not fill in missing ages, injuries, locations, or weather with averages or zeros. In cleaning, fix only clear errors (age -59; age 0 for non-passengers) by setting those ages to missing, and add simple flags and groups. In integration, keep every crash, use the Crashes date to assign weather, and build separate person-level, crash-level, and daily tables. Be careful with almost-empty fields (`lane_cnt`, `cell_phone_use`) and with UNKNOWN categories.

The raw data are good enough to use for this project if these limits are respected and documented.
