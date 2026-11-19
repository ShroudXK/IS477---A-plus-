# Status Report

This interim report for *Chicago Traffic Safety: Weather, Crash Frequency, and Injury Patterns* is current as of November 19, 2026. Acquisition, quality assessment, cleaning, and integration are complete; later quality assessment, analysis, documentation, and the final report remain.

## Task Progress

1. **Confirm scope and responsibilities** (completed October 22). The team agreed on the four research questions, the 2023–2024 Chicago and NOAA scope, and the roles in [`ProjectPlan.md`](ProjectPlan.md) and [`README.md`](README.md).

2. **Verify dataset feasibility** (completed October 30 by Yifei Zhang and Eric Xu). The three sources share usable linkage fields (`crash_record_id` and calendar date) and cover the study period.

3. **Acquire and document data** (completed November 16–18, later than November 6). We froze a raw snapshot of 222,810 crashes, 491,892 people, and the full NOAA O'Hare file (29,249 rows) in the [IS477 raw data](https://uofi.box.com/s/alz9j0cq7p33m014fe2qy86cptyg7kau) Box folder. [`scripts/download_data.py`](scripts/download_data.py) writes the files to `data/raw/` and checks SHA-256 values in [`data/raw/checksums.sha256`](data/raw/checksums.sha256) and [`data/raw/acquisition_log.json`](data/raw/acquisition_log.json).

4. **Assess source data quality** (completed November 18 by Yifei Zhang). See [`WorkLog.md`](WorkLog.md) (Dataset Quality Assessment) and [`scripts/Data quality Assessment.py`](scripts/Data%20quality%20Assessment.py). The assessment confirmed unique IDs, complete 2023–2024 crash dates, 731 complete weather days, and issues later handled in cleaning and integration: invalid ages and coordinates, 509 crashes with no People rows, and cross-table disagreements.

5. **Clean datasets** (completed November 18–19). Jacob Lee wrote [`scripts/clean_data.py`](scripts/clean_data.py). Eric Xu checked it against the quality assessment, fixed pandas default-NA parsing and float-cast IDs and ages, and updated the documentation, `.gitignore`, and pinned dependencies. All crash and person rows were kept (222,810 and 491,892); weather was filtered to 731 study-period days. See [`WorkLog.md`](WorkLog.md) (Data Cleaning), [`data/clean/cleaning_summary.json`](data/clean/cleaning_summary.json), and the [IS477_clean_data](https://uofi.box.com/s/fkrjtcdoowhcme7po5cvf3kdi145cld0) Box copy, which the workflow regenerates.

6. **Integrate datasets** (completed November 19 by Eric Xu). [`scripts/integrate_data.py`](scripts/integrate_data.py) joins people to crashes on `crash_record_id` and weather on the Crashes calendar date, writing `person_level.csv` (491,892 rows), `crash_level.csv` (222,810), `daily.csv` (731), and [`data/integrated/cross_table_review.csv`](data/integrated/cross_table_review.csv) (340 crashes). People-to-crash and crash-to-weather matches are 100%; 99.77% of crashes (222,301 / 222,810) have at least one person. [`scripts/run_all.py`](scripts/run_all.py) runs download, quality assessment, cleaning, and integration in order. A fresh clone finished in about 31 seconds with all 24 checks passing. See [`data/integrated/integration_summary.json`](data/integrated/integration_summary.json) and [`WorkLog.md`](WorkLog.md) (Data Integration).

7. **Assess integrated data quality** (not started; due November 21). Yifei Zhang will assess the four quality dimensions on the integrated tables, including match rates and the 340 flagged records.

8. **Analyze and visualize** (not started; due November 25). Proposed role-aligned leads, to be confirmed by the team: Q1, Eric Xu, daily crashes vs. precipitation (`daily.csv`); Q2, Jacob Lee, injuries by roadway user type, using cleaned person categories; Q3, Yifei Zhang, injuries by age group, tied to the age quality checks; Q4, Jiacheng Lin, user-type injuries by precipitation, tying findings into the final report. Q2–Q4 use `person_level.csv`.

9. **Document and reproduce the workflow** (in progress; due November 26). The automated workflow, pinned [`requirements.txt`](requirements.txt), and README reproduction steps are done. The data dictionary and machine-readable metadata are still needed (Jiacheng Lin and Eric Xu).

10. **Review ethics and limitations** (not started; due November 27). The team will review privacy, bias, coverage gaps, and interpretation limits, including single-station weather and the 509 crashes with no People records.

11. **Complete the final report and submission** (in planning; due November 27). Jiacheng Lin has reviewed the quality and cleaning write-ups. The report will explain why crashes without People records still count in daily totals and why missing injury values should not be treated as “no injury,” and will include findings for all four questions once the tables and figures are finalized.

## Updated Timeline

| Original Target | Updated / Actual | Task | Owner(s) | Status |
| --- | --- | --- | --- | --- |
| Oct. 30 | Oct. 22 | Confirm scope and responsibilities | All members | Completed |
| Oct. 30 | Oct. 30 | Verify dataset feasibility | Yifei Zhang; Eric Xu | Completed |
| Nov. 6 | Nov. 16–18 | Acquire and document data | All members | Completed |
| Nov. 13 | Nov. 18 | Assess source data quality | Yifei Zhang | Completed |
| Nov. 13 | Nov. 18–19 | Clean datasets | Jacob Lee; Eric Xu | Completed |
| Nov. 13 | Nov. 19 | Integrate datasets | Eric Xu | Completed |
| Nov. 13 | Nov. 21 | Assess integrated data quality | Yifei Zhang | Not started |
| Nov. 20 | Nov. 25 | Analyze and visualize | All members | Not started |
| Nov. 20 | Nov. 26 | Document and reproduce workflow | Jiacheng Lin; Eric Xu | In progress |
| Nov. 27 | Nov. 27 | Review ethics and limitations | All members | Not started |
| Nov. 27 | Nov. 27 | Complete the final report and submission | Jiacheng Lin; all members | In planning |

Completed dates are actual. Remaining targets stay on or before November 27, our original final-report date (Canvas deadlines are not in the course instructions).

## Changes to the Project Plan

Instructor feedback on Milestone 2 was: "Congrats. That is a great plan. Good research questions and well-described datasets." No revisions were requested, so the research questions and datasets are unchanged.

Four updates during execution:

(a) **Cleaning roles.** Data Cleaning is now shared by Jacob Lee and Eric Xu. Integration checks found that pandas' default NA rules and float-casting of IDs and ages would have distorted the cleaned People file. Eric fixed those issues on top of Jacob's script; see [`WorkLog.md`](WorkLog.md) (Data Cleaning).

(b) **Integration outputs.** The plan called for two analysis tables. The workflow now produces three (`crash_level.csv`, `person_level.csv`, and `daily.csv`) plus [`cross_table_review.csv`](data/integrated/cross_table_review.csv), so each question has the right unit of analysis.

(c) **Automation.** Instead of OpenRefine, [`scripts/run_all.py`](scripts/run_all.py) calls the single-purpose stage scripts in order. Reproduction requires no manual steps.

(d) **Data storage.** Raw and cleaned CSVs exceed GitHub's 100 MB limit, so they are hosted on UIUC Box and retrieved with SHA-256 verification.

## Challenges and Resolutions

1. **Pandas default NA parsing and float-cast IDs and ages.** Literal `"NA"` was read as missing, and IDs and ages were written as decimals, so a text join on `vehicle_id` would have failed. [`scripts/clean_data.py`](scripts/clean_data.py) now treats only blank cells as missing and stores IDs as text and ages as nullable whole numbers.

2. **Cross-table inconsistencies (X2–X5).** Timestamps, injury totals, and severity disagree for some crashes. Deleting or “correcting” these rows would hide the conflict and could bias results. The 340 affected crashes are flagged in [`cross_table_review.csv`](data/integrated/cross_table_review.csv) and kept as recorded.

3. **Large CSVs over GitHub's 100 MB limit.** Raw and cleaned crash and people files are hosted on Box, downloaded by [`scripts/download_data.py`](scripts/download_data.py), and checked with SHA-256 hashes before later steps run.

4. **Single-station weather and unmatched crashes.** All weather comes from one O'Hare station, and 509 crashes (0.23%) have no People records. Analysis will treat the weather as a city-wide daily summary, keep the 509 crashes in daily counts but not in injury proportions, and, when needed, report results with and without the 340 flagged records.

5. **Tight schedule after integration.** Quality assessment, cleaning, and integration finished on November 18–19, later than the November 13 target, leaving less time for the remaining quality check, analysis, and data dictionary. We shifted those targets and proposed role-aligned question leads so work can proceed in parallel.

## Team Contributions

*Each teammate should review, revise if needed, and personally commit their paragraph below before the team creates the `status-report` tag.*

**Eric Xu.** I lead data integration and contributed follow-up cleaning. I added the Box download script and SHA-256 checks, reviewed Jacob's cleaning against Yifei's assessment, and fixed pandas default-NA parsing and float-cast IDs and ages in `scripts/clean_data.py`. I pinned package versions, updated `.gitignore`, wrote `scripts/integrate_data.py` and `scripts/run_all.py`, verified a fresh-clone rerun, and wrote the Data Cleaning (continued) and Data Integration sections now archived in [`WorkLog.md`](WorkLog.md).

**Jacob Lee.** I lead data cleaning. I wrote the first version of `scripts/clean_data.py`, keeping all crash and person records, correcting invalid coordinates and impossible ages, adding age groups and an injured flag, and filtering weather to 731 study-period days. I documented these decisions in [`WorkLog.md`](WorkLog.md) (Data Cleaning) and handed cross-table issues to integration.

**Yifei Zhang.** I lead data quality assessment. I assessed accuracy, completeness, timeliness, and consistency on the raw files, wrote [`scripts/Data quality Assessment.py`](scripts/Data%20quality%20Assessment.py), and recorded the findings in [`WorkLog.md`](WorkLog.md) (Dataset Quality Assessment) to guide cleaning and integration. Next, I will assess the integrated tables.

**Jiacheng Lin.** I lead the final data report. I have reviewed the quality and cleaning sections and identified two decisions the report needs to explain: why crashes without matching person records still count toward daily crash totals, and why missing injury information should not be treated as “no injury.” Next, I will compile findings for all four research questions once the tables and figures are finalized.
