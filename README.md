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
| Eric Xu | Data Integration |
| Jacob Lee | Data Cleaning |
| Yifei Zhang | Data Quality Assessment |
| Jiacheng Lin | Final data report |

All members will also review the integrated data, analysis, and final deliverables. Each member will lead the analysis for one of the four research questions.

## Workflow

The planned workflow is:

1. Acquire the datasets from their official sources.
2. Verify SHA-256 checksums of the downloaded files.
3. Assess data quality.
4. Clean the datasets.
5. Integrate the cleaned datasets and check quality again after the joins.
6. Analyze the research questions and document the work.

## Planned repository structure

```
README.md           Project introduction (the final report will later be written here)
ProjectPlan.md      Project plan
StatusReport.md     Interim status report
scripts/            Code for acquisition, quality checks, cleaning, integration, and analysis
data/raw/           Checksums and download log; raw CSVs are downloaded here by scripts/download_data.py (not committed)
data/clean/         Cleaned tables; large CSV files are not committed
data/integrated/    Combined, analysis-ready tables; large CSV files are not committed
reports/            Quality, cleaning, and integration reports
docs/               Source notes and related documentation
```

## Current status

This project is in the interim stage (Milestone 3). The project plan is in [`ProjectPlan.md`](ProjectPlan.md). An interim status report has been started in [`StatusReport.md`](StatusReport.md) and is still being written. Work on data acquisition, quality assessment, cleaning, and integration is in progress. Analysis, final documentation, and the final report will come later.

## Data terms

This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago. The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site. The data provided at this site is subject to change at any time. It is understood that the data provided at this site is being used at one's own risk.
