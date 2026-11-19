# Project Plan

**Project Title:** Chicago Traffic Safety: Weather, Crash Frequency, and Injury Patterns  
**Course:** IS 477  
**Team:** Eric Xu, Jacob Lee, Yifei Zhang, Jiacheng Lin  

## Overview


For our project, we want to look at how daily weather conditions are related to traffic crashes and injuries in Chicago. Rain, snow, and extreme temperatures can affect driving conditions, so we thought it would be interesting to see whether traffic accidents happen more often or lead to more injuries under certain weather conditions. We also want to see whether injury patterns differ by roadway user type and age group.

We plan to use three datasets: Chicago Traffic Crashes - Crashes, NOAA Daily Weather, and Chicago Traffic Crashes - People. We will focus on traffic accidents reported in Chicago between 2023 and 2024.

Our plan is to:

1. Download the three datasets from their official sources and review the information provided about them.
2. Check the data for missing values, duplicates, and other possible issues.
3. Clean the datasets and make sure dates, identifiers, and categories are in consistent formats.
4. Combine the People and Crashes datasets using crash IDs, then add daily weather observations using dates.
5. Compare daily crash counts under different weather conditions and injury proportions across roadway user types and age groups.
6. Track our steps and explain how we handled the data so anyone can repeat our work

By the end of the project, we hope to have a combined dataset, a data dictionary, visualizations, and code that can reproduce our results. Our main focus is making sure the data is collected, cleaned, and combined properly before looking at any patterns.

## Team

The following roles are proposed and will be confirmed by the team. All members will review the integrated data, analysis, and final deliverables.

| Team Member | Proposed Role | Planned responsibilities |
| --- | --- | --- |
| Eric Xu | Data Integration; Data Cleaning (continued) | Integrate the Crashes, People, and NOAA weather datasets using crash IDs and dates, validate the joins, and prepare analysis-ready tables with reproducible code. After the first-pass cleaning, complete follow-up fixes needed for integration and reproducibility. Proposed lead for research question 1. |
| Jacob Lee | Data Cleaning | Clean the datasets by handling missing values, removing duplicates, and fixing inconsistent formats to prepare the data for integration. Proposed lead for research question 2. |
| Yifei Zhang | Data Quality Assessment | Assess the quality of the three datasets by checking accuracy, completeness, timeliness, and consistency. Identify missing values, duplicates, and inconsistencies before integration, and evaluate the quality of the combined dataset after integration. Proposed lead for research question 3. |
| Jiacheng Lin | Final data report | Write the final data report, summarize the main findings, explain data cleaning and integration decisions, discuss constraints and limitations, and coordinate with teammates to review the report before submission. Proposed lead for research question 4. |

In addition to these roles, each member will lead one of the four research questions and complete its analysis, visualizations, and written findings. The proposed, role-aligned assignment, to be confirmed by the team, is: Q1, Eric Xu (daily crashes vs. precipitation, using `daily.csv`); Q2, Jacob Lee (injuries by roadway user type); Q3, Yifei Zhang (injuries by age group); and Q4, Jiacheng Lin (user-type injuries by precipitation).

## Research or Business Questions:

1. **Primary question:** How does the average daily number of reported traffic crashes in Chicago differ between days with and without precipitation?

2. **Supporting question:** Among people involved in reported crashes, how does the proportion sustaining injuries differ among drivers, passengers, pedestrians, and cyclists?

3. **Supporting question:** How does the proportion of injured people vary across age groups among those involved in reported crashes?

4. **Supporting question:** Do injury proportions for different roadway user types vary between days with and without precipitation?

**Unit of analysis:** We will mainly look at individual crash records and the people involved in each accident. For the first question, we will group crashes by date to see how the average number of crashes differs between days with and without precipitation. We will also use the People dataset to look at injuries among different groups of people.

**Scope:** Our project will focus on traffic crashes reported in Chicago from 2023 to 2024. We plan to use records that have enough information to connect the three datasets. Some records might have missing information, so we will check those cases and explain how we deal with them.

**Contribution of integration:** Datasets give us information that we need for our project. The crash data tells us when accidents happened. The NOAA data shows the weather conditions on those days. The People dataset gives us details about the people, such as their ages, whether they were drivers or passengers, and whether they were injured. By putting these datasets together, we can look at how weather conditions are related to the number of crashes and compare injuries among different groups of people.

## Datasets

We will use three complementary datasets covering January 1, 2023 through December 31, 2024. Together, they describe reported crashes, the people involved, and daily weather conditions. The two Chicago datasets provide different levels of detail, while NOAA adds independent weather measurements. All three can be acquired as tabular data and integrated using Python and pandas.

### 1. Chicago Traffic Crashes - Crashes

**Source:** [Traffic Crashes - Crashes, Chicago Data Portal](https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if/about_data)  
**Publisher:** City of Chicago; data provided by the Chicago Police Department.  
**Unit of observation:** One reported traffic crash.

This dataset provides the time, location, circumstances, and reported outcomes of traffic crashes in Chicago. We will download records for 2023-2024 through the portal's API or CSV export.

| Feature | Description and planned use |
| --- | --- |
| `CRASH_RECORD_ID` | Unique crash identifier; links each crash to records in the People dataset and supports counting distinct crashes. |
| `CRASH_DATE` | Crash date and time; used to derive a calendar date for joining NOAA observations and calculating daily crash counts. |
| `INJURIES_TOTAL`, `MOST_SEVERE_INJURY` | Crash-level injury outcomes; used to summarize reported injuries and compare them with person-level outcomes. |
| `WEATHER_CONDITION` | Weather recorded in the crash report; provides context alongside NOAA's measured daily conditions. |
| `LIGHTING_CONDITION`, `ROADWAY_SURFACE_COND` | Reported lighting and road-surface conditions; provide additional context for interpreting results. |
| `CRASH_HOUR`, `CRASH_DAY_OF_WEEK` | Time-related features available for descriptive summaries of when crashes occur. |

This dataset supports our primary question about average daily crash counts on days with and without precipitation. It also supplies the crash context needed to interpret injuries recorded in the People dataset.

### 2. Chicago Traffic Crashes - People

**Source:** [Traffic Crashes - People, Chicago Data Portal](https://data.cityofchicago.org/Transportation/Traffic-Crashes-People/u6pd-qa9d)  
**Publisher:** City of Chicago; data provided by the Chicago Police Department.  
**Unit of observation:** One person involved in a reported crash.

This dataset describes drivers, passengers, pedestrians, cyclists, and other roadway users involved in crashes. It adds individual characteristics and injury outcomes that are not available at the same level of detail in the Crashes dataset. We will retrieve records for the same 2023-2024 period using the API or CSV export.

| Feature | Description and planned use |
| --- | --- |
| `PERSON_ID` | Unique person-record identifier; supports person-level counting and duplicate checks. |
| `CRASH_RECORD_ID` | Identifies the associated crash; used to join person records to the Crashes dataset. |
| `PERSON_TYPE` | Roadway user category; used to compare drivers, passengers, pedestrians, and cyclists. |
| `AGE` | Age of the person; used to create age groups and compare injury proportions. |
| `INJURY_CLASSIFICATION` | Reported injury severity; used to calculate injury proportions among recorded people. |
| `SAFETY_EQUIPMENT`, `AIRBAG_DEPLOYED` | Additional safety-related features available for supplementary descriptive summaries. |

This dataset supports our questions about differences in injury proportions across roadway user types and age groups. After integration with crash dates and NOAA observations, it also allows comparisons of injury proportions across daily precipitation categories.

### 3. NOAA Daily Weather - Chicago O'Hare

**Source:** [NOAA GHCN Daily Summaries, Chicago O'Hare International Airport](https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00094846/detail)  
**Data file:** [O'Hare Daily Summaries CSV](https://www.ncei.noaa.gov/data/daily-summaries/access/USW00094846.csv)  
**Publisher:** NOAA National Centers for Environmental Information.  
**Station:** `USW00094846`.  
**Unit of observation:** One day of observations at the selected station in the Daily Summaries CSV.

We will select daily observations for 2023-2024 from NOAA's Global Historical Climatology Network Daily dataset. These measurements add quantitative weather information to the crash and person records.

| Feature | Description and planned use |
| --- | --- |
| `STATION`, `DATE` | Identify the station and observation date; `DATE` is the linkage field for the crash data. |
| `PRCP` | Daily precipitation amount; the main weather variable used to distinguish days with and without measured precipitation. |
| `SNOW`, `SNWD` | Daily snowfall and snow depth; available for supplementary weather descriptions. |
| `TMAX`, `TMIN` | Daily maximum and minimum temperatures; available for descriptive summaries and temperature-based comparisons. |

The main analysis will use `PRCP` to classify days by precipitation and compare average daily crash counts. The other weather features provide additional context without requiring a separate dataset.

### How the Datasets Connect

We will first join the People dataset to the Crashes dataset using `CRASH_RECORD_ID`. This is a many-to-one join from people to crashes: several people can belong to the same crash. We will then extract the calendar date from `CRASH_DATE` and join it to NOAA's `DATE`, with one weather record per station-day. Each person in the integrated table will therefore have their individual characteristics, the associated crash information, and the daily weather measurements.

We retain three analysis tables: a crash-level table with one row per crash, a person-level table with one row per person, and a daily table with one row per study-period day. The daily table is aligned with the full study calendar for crash-count comparisons. The person-level table supports injury comparisons by roadway user type, age group, and precipitation category. This structure allows all three datasets to contribute while preserving the correct counting unit for each research question.

## Timeline

| Original Target | Updated / Actual | Task | Description / Deliverable | Responsible Member(s) | Status |
| --- | --- | --- | --- | --- | --- |
| Oct. 30 | Oct. 22 | Confirm scope and responsibilities | Finalize the scope, roles, and requirements checklist. Each member will lead one of the four research questions, with one analysis lead per question. | All members | Completed |
| Oct. 30 | Oct. 30 | Verify dataset feasibility | Check access, provenance, reuse terms, coverage, and compatible linkage fields. | Yifei Zhang; Eric Xu | Completed |
| Nov. 6 | Nov. 16–18 | Acquire and document data | Download the three datasets for 2023–2024, verify SHA-256 checksums, and document sources and variable definitions. | All members | Completed |
| Nov. 13 | Nov. 18 | Assess source data quality | Before cleaning and integration, assess accuracy, completeness, timeliness, and consistency, and document the issues to address. | Yifei Zhang | Completed |
| Nov. 13 | Nov. 18–19 | Clean datasets | Handle missing values, duplicates, invalid values, and inconsistent formats, and document cleaning decisions. Eric Xu completed follow-up fixes needed for integration. | Jacob Lee; Eric Xu | Completed |
| Nov. 13 | Nov. 19 | Integrate datasets | Join the cleaned datasets using crash IDs and dates, validate the joins, and prepare crash-level, person-level, and daily analysis tables, plus a cross-table review list. | Eric Xu | Completed |
| Nov. 13 | Nov. 21 | Assess integrated data quality | After integration, assess the four quality dimensions and review matching rates, row counts, and unmatched records with Eric. | Yifei Zhang | Not started |
| Nov. 20 | Nov. 25 | Analyze and visualize | Each member will analyze their selected research question, create supporting tables and visualizations, and write up their methods and findings. | All members; one question per member | Not started |
| Nov. 20 | Nov. 26 | Document and reproduce workflow | Complete the data dictionary, source citations, dependency information, automated workflow, and reproduction instructions. The run-all workflow and reproduction instructions are done; the data dictionary and metadata remain. | Jiacheng Lin; Eric Xu | In progress |
| Nov. 27 | Nov. 27 | Review ethics and limitations | Assess privacy, bias, coverage gaps, interpretation limits, and data-sharing restrictions. | All members | Not started |
| Nov. 27 | Nov. 27 | Complete the final report and submission | Jiacheng will compile the report from all members' contributions. The team will review findings, verify reproducibility, check course requirements, and finalize the submission. | Jiacheng Lin; all members | In planning |

## Constraints

| Potential Constraint | Project-Specific Details to Confirm | Planned Response |
| --- | --- | --- |
| Access and reuse restrictions | Download limits, API requirements, and reuse terms for the Chicago and NOAA datasets still need to be checked. These requirements may affect how we collect and share the data. | Check each source’s access requirements and reuse terms before downloading. Record source URLs and retrieval dates, and share data only as permitted. |
| Data quality and completeness | Crash and People records may have missing ages, injury information, dates, or locations. Weather records may also contain missing observations. These gaps could affect comparisons between groups.| Check for missing values and duplicates. Keep unknown values separate from confirmed “no injury” or “no precipitation” values, and report any records excluded from each analysis. |
| Integration compatibility | Crash records, individual People records, and daily weather observations represent different units. Joining them could repeat crash records and lead to incorrect crash counts. | Confirm the shared crash identifier for the Crash and People datasets and match weather by date. Count unique crashes for crash totals and use person-level records for injury proportions. |
| Temporal and spatial coverage | The project only covers reported Chicago crashes from 2023 to 2024. Weather conditions at the selected NOAA station may differ from conditions at individual crash locations, and daily measurements cannot show the exact weather at the time of a crash.| Check weather coverage for the study period, document station selection, and explain the limits of matching daily weather to individual crashes. Limit conclusions to the selected location and period.|
| Ethical concerns and bias | The data covers people involved in reported crashes, so it does not represent every road user or every crash. Small groups defined by age, location, or road user type could also raise privacy concerns. | Present grouped results, avoid publishing detailed individual records, and combine or omit very small groups where needed. Explain that injury proportions apply to people in reported crashes. |
| Technical and interpretation limits | The team has limited time and computing resources. Differences in crash counts may also reflect traffic volume, holidays, or other factors beyond precipitation. Without traffic exposure data, crash counts cannot directly measure the risk of crashing per trip.| Keep the analysis focused on the research questions and the 2023–2024 period. Describe results as associations and avoid claiming that precipitation causes crashes or that one group is inherently less safe. |

## Gaps

Several earlier gaps have now been checked, and a few items remain.

Weather Data Coverage: The NOAA O'Hare file has complete daily observations for all 731 days in 2023–2024, including 2024-02-29, with no missing PRCP, TMAX, TMIN, SNOW, or SNWD values. We still treat these observations as a city-wide daily summary, not the exact condition at the crash time or location.

Data Quality: Pre-integration quality has been assessed for accuracy, completeness, timeliness, and consistency; the findings are in [`WorkLog.md`](WorkLog.md). The post-integration four-dimension quality assessment of the combined tables is still outstanding and is scheduled for November 21.

Data Integration: Joins have been validated. Every person matches a crash (491,892 / 491,892, 100%), every crash date matches an O'Hare weather day (222,810 / 222,810, 100%), and 99.77% of crashes (222,301 / 222,810) have at least one person. The remaining 509 crashes are kept in daily counts, and a 340-row review list records cross-table disagreements.

Workflow and Reproducibility: `scripts/run_all.py` now automates acquisition, quality assessment, cleaning, and integration from a fresh clone, with SHA-256 checks and pinned dependencies. Analysis scripts, a data dictionary, and machine-readable metadata are still needed.

We will continue to address the remaining gaps as we work with the datasets and document any important decisions or changes in our GitHub repository.
