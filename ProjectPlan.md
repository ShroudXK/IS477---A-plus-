# Project Plan

**Project Title:** [Enter project title]  
**Course:** IS 477  
**Team:** Eric Xu, Jacob Lee, Yifei Zhang, Jiacheng Lin  
**Status:** Initial framework; replace bracketed placeholders before submission.

## Overview

[Describe the overall project goal, why it matters, and the intended audience.]

We aim to answer [main question] by integrating three complementary datasets about [topic] at the [unit of analysis] level, covering [geographic area] during [time period].

Our planned approach is to:
1. Identify appropriate original data sources and verify their provenance, access conditions, and reuse permissions.
2. Acquire the datasets and document their structure, variables, and collection methods.
3. Clean and standardize the data, including missing values, duplicates, identifiers, and inconsistent formats.
4. Integrate the datasets using [shared identifiers or attributes].
5. Analyze [key variables or relationships] and create visualizations that address our questions.
6. Document the workflow, limitations, and findings so that others can reproduce the project.

**Expected outputs:** [Integrated dataset, data dictionary, reproducible scripts or notebooks, visualizations, and final report.]

*Keep the completed Overview at 250 words or fewer.*

## Team

The following roles are proposed and will be confirmed by the team. All members will review the integrated data, analysis, and final deliverables.

| Team Member | Proposed Role | Planned Responsibilities |
| --- | --- | --- |
| Eric Xu | Project coordination and integration | Track milestones, coordinate contributions, define integration keys, and combine the cleaned datasets. |
| Jacob Lee | Data acquisition and provenance | Locate original sources, acquire data, and document collection methods, access dates, and reuse conditions. |
| Yifei Zhang | Data cleaning and quality | Standardize variables, address missing values and duplicates, and document data quality checks. |
| Jiacheng Lin | Analysis and communication | Develop visualizations, summarize findings, and coordinate the final report and presentation. |

## Research or Business Question(s)

1. **Primary question:** [What main question will the integrated data answer?]
2. **Supporting question:** [How does the outcome vary across groups, locations, or time periods?]
3. **Supporting question:** [What relationship between variables from different datasets will be examined?]

**Unit of analysis:** [For example, one county per year.]  
**Scope:** [Population, geography, time period, and inclusion/exclusion criteria.]  
**Contribution of integration:** [Explain why answering these questions requires information from all three datasets.]

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
