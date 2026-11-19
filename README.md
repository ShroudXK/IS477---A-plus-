# Chicago Traffic Safety: Weather, Crash Frequency, and Injury Patterns

This is the public repository for our IS 477 group project.

## Overview

This project looks at how daily weather and driving conditions are related to traffic crashes and injuries in Chicago. We combine two Chicago Data Portal datasets on reported crashes and the people involved in them, covering 2023–2024, with daily weather observations from the NOAA GHCN-Daily station at O'Hare International Airport. Our aim is to see whether crashes happen more often, or lead to more injuries, on days with certain weather conditions, and whether injury patterns differ by roadway user type and age group.

## Research questions

1. **Primary question:** How does the average daily number of reported traffic crashes in Chicago differ between days with and without precipitation?

2. **Supporting question:** Among people involved in reported crashes, how does the proportion sustaining injuries differ among drivers, passengers, pedestrians, and cyclists?

3. **Supporting question:** How does the proportion of injured people vary across age groups among those involved in reported crashes?

4. **Supporting question:** Do injury proportions for different roadway user types vary between days with and without precipitation?

## Datasets

We use three complementary datasets. The Chicago crash and people records are joined by crash ID. Daily weather is then joined by date.

| Dataset | Source | Link |
| --- | --- | --- |
| Chicago Traffic Crashes — Crashes (`85ca-t3if`) | Chicago Data Portal; City of Chicago / Chicago Police Department | [Crashes dataset](https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if/about_data) |
| Chicago Traffic Crashes — People (`u6pd-qa9d`) | Chicago Data Portal; City of Chicago / Chicago Police Department | [People dataset](https://data.cityofchicago.org/Transportation/Traffic-Crashes-People/u6pd-qa9d) |
| NOAA GHCN-Daily, Chicago O'Hare (`USW00094846`) | NOAA National Centers for Environmental Information | [DOI 10.7289/V5D21VHZ](https://doi.org/10.7289/V5D21VHZ); [station page](https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00094846/detail); [daily summaries CSV](https://www.ncei.noaa.gov/data/daily-summaries/access/USW00094846.csv) |

## Data snapshot and access

The Chicago crash and people datasets are updated daily on the Chicago Data Portal, and the NOAA file is also updated regularly. To keep our results reproducible, we froze one snapshot of all three raw files and use it as the fixed input for the whole workflow. Re-downloading from the live sources later may give different rows and different checksums.

| File | Downloaded (UTC) | Query | Rows | SHA-256 |
| --- | --- | --- | --- | --- |
| `crashes_2023_2024.csv` | 2026-11-16 18:15 | `crash_date` from 2023-01-01 to 2024-12-31 | 222,810 | `0e5fa1cc…023490` |
| `people_2023_2024.csv` | 2026-11-16 18:19 | `crash_date` from 2023-01-01 to 2024-12-31 | 491,892 | `85157f9c…6a39fdf` |
| `noaa_usw00094846.csv` | 2026-11-16 18:19 | full station file | 29,249 | `b271731e…c3adcf` |

The full checksums are in [`data/raw/checksums.sha256`](data/raw/checksums.sha256), and the source URL, query, time, and row count for each file are in [`data/raw/acquisition_log.json`](data/raw/acquisition_log.json).

**Where the files are.** All three raw CSV files, including the NOAA file, are stored in a shared Box folder: [IS477 raw data snapshot](https://uofi.box.com/s/alz9j0cq7p33m014fe2qy86cptyg7kau). They are not committed to this repository. The first step of the workflow is:

```
python scripts/download_data.py
```

This script downloads the files from Box into `data/raw/` and verifies every SHA-256 checksum before any later step runs. If a checksum does not match, the workflow stops. To fetch the data by hand instead, download all files from the Box folder and place them in `data/raw/`.

## Team

| Team member | Role |
| --- | --- |
| Eric Xu | Data Cleaning (continued); Data Integration |
| Jacob Lee | Data Cleaning |
| Yifei Zhang | Data Quality Assessment |
| Jiacheng Lin | Final data report |

All members will also review the integrated data, analysis, and final deliverables. Each member will lead the analysis for one of the four research questions.

## Workflow

The workflow is a chain of separate, single-purpose scripts, run in this order by [`scripts/run_all.py`](scripts/run_all.py):

| Step | Script | Input | Output |
| --- | --- | --- | --- |
| 1. Acquire and verify | [`scripts/download_data.py`](scripts/download_data.py) | Box snapshot | `data/raw/*.csv` (SHA-256 checked) |
| 2. Assess quality | [`scripts/Data quality Assessment.py`](scripts/Data%20quality%20Assessment.py) | `data/raw/` | Printed quality report (read-only) |
| 3. Clean | [`scripts/clean_data.py`](scripts/clean_data.py) | `data/raw/` | `data/clean/` + `cleaning_summary.json` |
| 4. Integrate | [`scripts/integrate_data.py`](scripts/integrate_data.py) | `data/clean/` | `data/integrated/` + `integration_summary.json` |
| 5. Analyze | to be added | `data/integrated/` | results |

Steps 3 and 4 check their own results (row counts, join match rates, and the cross-table counts from the quality assessment) and stop with an error if anything is different. The technical details are in [`WorkLog.md`](WorkLog.md) (Data Quality Assessment, Data Cleaning, Data Cleaning (continued), and Data Integration); [`StatusReport.md`](StatusReport.md) holds the concise Milestone 3 interim status report.

## How to reproduce

The workflow was tested with **Python 3.13** on Linux. Package versions are pinned in [`requirements.txt`](requirements.txt). From a terminal:

```
git clone https://github.com/ShroudXK/IS477---A-plus-.git
cd IS477---A-plus-
python3 -m venv .venv               # use Python 3.13
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_all.py
```

No other steps or edits are needed. All paths are relative to the project folder. The full run takes about one minute, most of it downloading about 400 MB from Box. Each step can also be run on its own in the order above, for example `python scripts/integrate_data.py`.

**Cleaned data on Box (optional).** For convenience, a copy of the cleaned tables is in the Box folder [IS477_clean_data](https://uofi.box.com/s/fkrjtcdoowhcme7po5cvf3kdi145cld0). You do not need it to reproduce our results, because `scripts/clean_data.py` regenerates the same files. Compare them with the SHA-256 values in [`data/clean/cleaning_summary.json`](data/clean/cleaning_summary.json).

## Repository structure

```
README.md              Project introduction (the final report will later be written here)
ProjectPlan.md         Project plan
StatusReport.md        Milestone 3 interim status report (progress, timeline, changes, challenges, contributions)
WorkLog.md             Full technical work log (quality assessment, cleaning, integration, final report notes)
requirements.txt       Pinned Python packages
scripts/
  run_all.py                    Runs the whole workflow in order
  download_data.py              Step 1: download raw data from Box and check SHA-256
  Data quality Assessment.py    Step 2: quality assessment of the raw data
  clean_data.py                 Step 3: cleaning
  integrate_data.py             Step 4: integration and cross-table checks
data/raw/              Checksums and download log; raw CSVs are downloaded here (not committed)
data/clean/            Cleaned tables (CSVs not committed) and cleaning_summary.json
data/integrated/       person_level, crash_level, and daily tables (CSVs not committed),
                       cross_table_review.csv, and integration_summary.json
```

## Current status

This project is in the interim stage (Milestone 3). The project plan is in [`ProjectPlan.md`](ProjectPlan.md), and the interim status report is in [`StatusReport.md`](StatusReport.md). Data acquisition, quality assessment, cleaning, and integration are finished and run end to end with `scripts/run_all.py`. The post-integration quality assessment, the analysis, the final documentation, and the final report will come next.

## Data terms

This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago. The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site. The data provided at this site is subject to change at any time. It is understood that the data provided at this site is being used at one's own risk.
