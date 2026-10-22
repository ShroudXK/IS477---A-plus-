# Project Plan

**Project Title:** [Enter project title]  
**Course:** IS 477  
**Team:** Eric Xu, Jacob Lee, Yifei Zhang, Jiacheng Lin  
**Status:** Initial framework; replace bracketed placeholders before submission.

## Overview


For our project, we want to look at how daily weather conditions are related to traffic crashes and injuries in Chicago. Rain, snow, and extreme temperatures can affect driving conditions, so we thought it would be interesting to see whether traffic accidents happen more often or lead to more injuries under certain weather conditions. We also want to see whether these patterns differ by location.

We plan to use three datasets: Chicago Traffic Crashes, NOAA Daily Weather, and Chicago Traffic Crashes. We will focus on traffic accidents reported in Chicago between 2023 and 2024.

Our plan is to:

1. Download the three datasets from their official sources and review the information provided about them.
2. Check the data for missing values, duplicates, and other possible issues.
3. Clean the datasets and make sure the dates and locations are in consistent formats.
4. Combine the weather and crash data using dates, and match crash locations with road segments.
5. Compare the number of crashes and reported injuries under different weather conditions and across road segments.
6. Track our steps and explain how we handled the data so anyone can repeat our work

By the end of the project, we hope to have a combined dataset, a data dictionary, visualizations, and code that can reproduce our results. Our main focus is making sure the data is collected, cleaned, and combined properly before looking at any patterns.

## Team

The following roles are proposed and will be confirmed by the team. All members will review the integrated data, analysis, and final deliverables.

| Team Member | Proposed Role | Planned Responsibilities |
| --- | --- | --- |
| Eric Xu | 。。。 | 。。。 |
| Jacob Lee | 。。。 | 。。。 |
| Yifei Zhang | 。。。 | 。。。 |
| Jiacheng Lin | 。。。 | 。。。 |

## Research or Business Question(s)

1. **Primary question:** How does the average daily number of reported traffic crashes in Chicago differ between days with and without precipitation?

2. **Supporting question:** Among people involved in reported crashes, how does the proportion sustaining injuries differ among drivers, passengers, pedestrians, and cyclists?

3. **Supporting question:** How does the proportion of injured people vary across age groups among those involved in reported crashes?

4. **Supporting question:** Do injury proportions for different roadway user types vary between days with and without precipitation?

**Unit of analysis:** We will mainly look at individual crash records and the people involved in each accident. For the first question, we will group crashes by date to see how the average number of crashes differs between days with and without precipitation. We will also use the People dataset to look at injuries among different groups of people.

**Scope:** Our project will focus on traffic crashes reported in Chicago from 2023 to 2024. We plan to use records that have enough information to connect the three datasets. Some records might have missing information, so we will check those cases and explain how we deal with them.

**Contribution of integration:** Each dataset gives us different information that we need for our project. The crash data tells us when accidents happened. The NOAA data shows the weather conditions on those days. The People dataset gives us more details about the people, such as their ages, whether they were drivers or passengers, and whether they were injured. By putting these datasets together, we can look at how weather conditions are related to the number of crashes and compare injuries among different groups of people.

## Datasets

Use at least three distinct, complementary datasets that can be meaningfully integrated. Do not use Kaggle as a data source.

| Detail | Dataset 1 | Dataset 2 | Dataset 3 |
| --- | --- | --- | --- |
| Dataset name | [Name] | [Name] | [Name] |
| Original publisher and source URL | [Publisher; URL] | [Publisher; URL] | [Publisher; URL] |
| Description and contribution | [Information provided; question supported] | [Different but related information; question supported] | [Different but related information; question supported] |
| Key variables | [Variables] | [Variables] | [Variables] |
| Unit of observation | [What one row represents] | [What one row represents] | [What one row represents] |
| Geographic and temporal coverage | [Area; period] | [Area; period] | [Area; period] |
| Format and access method | [CSV/API/etc.; access requirements] | [CSV/API/etc.; access requirements] | [CSV/API/etc.; access requirements] |
| Linkage attributes | [Identifier(s), geography, and/or time] | [Identifier(s), geography, and/or time] | [Identifier(s), geography, and/or time] |
| Provenance and reuse terms | [Collection method; license/terms] | [Collection method; license/terms] | [Collection method; license/terms] |

### Integration Plan

- **Target structure:** [What one row in the integrated dataset will represent.]
- **Dataset 1 + Dataset 2:** Join on [exact columns] using a [join type]; expected relationship: [one-to-one/one-to-many/etc.].
- **Combined data + Dataset 3:** Join on [exact columns] using a [join type]; expected relationship: [relationship].
- **Preparation:** [Align geographic boundaries, time periods, identifier formats, units, and aggregation levels.]
- **Validation:** Check key uniqueness, unmatched records, unexpected row duplication, and coverage before and after each join.
- **Unmatched records:** [Explain how unmatched records will be investigated, retained, or excluded and how exclusions will be reported.]

## Timeline

Dates and role assignments below are provisional. Replace the date placeholders with the course deadlines.

| Target Completion | Task | Description / Deliverable | Responsible Member(s) |
| --- | --- | --- | --- |
| Week 1 — [Date] | Confirm scope and requirements | Finalize questions, unit of analysis, roles, and the full assignment requirements checklist. | All members |
| Week 1 — [Date] | Verify dataset feasibility | Identify three sources; check access, provenance, reuse terms, coverage, and compatible linkage attributes. | Jacob; Eric |
| Week 2 — [Date] | Acquire and document data | Preserve raw files; record source URLs, retrieval dates, versions, and variable definitions. | Jacob |
| Week 3 — [Date] | Clean and validate data | Resolve format inconsistencies, duplicates, and missing values; document cleaning decisions and quality checks. | Yifei |
| Week 4 — [Date] | Integrate datasets | Implement joins and verify matching rates, row counts, and the target unit of analysis. | Eric; Yifei |
| Week 5 — [Date] | Analyze and visualize | Answer the research questions using appropriate summaries and visualizations. | Jiacheng; all members |
| Week 5 — [Date] | Document and reproduce workflow | Complete the data dictionary, source citations, environment/dependency information, and rerun instructions. | Jacob; Eric |
| Week 6 — [Date] | Review ethics and limitations | Assess privacy, bias, coverage gaps, interpretation limits, and any data-sharing restrictions. | All members |
| Week 6 — [Date] | Finalize and submit | Review findings, verify reproducibility, complete the report/presentation, and audit all course requirements. | Jiacheng; all members |

## Constraints

| Potential Constraint | Project-Specific Details to Confirm | Planned Response |
| --- | --- | --- |
| Access and reuse restrictions | [Licenses, API limits, login requirements, or redistribution restrictions.] | Verify terms before acquisition and document permitted uses. |
| Data quality and completeness | [Missing values, duplicates, inconsistent definitions, or uncertain provenance.] | Profile each source and document cleaning decisions and remaining issues. |
| Integration compatibility | [Different identifiers, time periods, geographic boundaries, or observation levels.] | Test linkage early and document harmonization or aggregation decisions. |
| Temporal and spatial coverage | [Areas, populations, or periods that are absent or incompatible.] | Define a feasible common scope and disclose exclusions. |
| Ethical concerns and bias | [Privacy risks, sensitive attributes, or underrepresented groups.] | Minimize sensitive information and avoid unsupported generalizations. |
| Technical and interpretation limits | [Processing resources, team capacity, or limits of observational analysis.] | Use a manageable scope and distinguish observed associations from causal claims. |

## Gaps

- [ ] Confirm the project topic, questions, and intended audience.
- [ ] Confirm team roles and actual milestone dates.
- [ ] Select three datasets and verify their original sources and reuse terms.
- [ ] Inspect sample records to confirm shared identifiers and compatible coverage.
- [ ] Decide how to handle missing data, unmatched records, and aggregation.
- [ ] Select analysis methods and visualizations appropriate to the questions.
- [ ] Review the full Requirements section referenced by the assignment; add any requirements not included in the provided instructions.
- [ ] Identify questions requiring instructor or team input: [List questions].

This plan will evolve as we inspect the data and learn later course topics. We will update our plans for metadata, data quality, integration, ethical reuse, reproducibility, and long-term preservation or sharing as needed, recording major decisions in the repository.
