# Data Cleaning

**Course:** IS 477
**Project:** Chicago Traffic Safety: Weather, Crash Frequency, and Injury Patterns
**Responsible Member:** Jacob Lee

## Overview

I cleaned the three datasets based on the issues identified in Yifei's data quality assessment. The main goal was to fix clearly incorrect values and keep as many records as possible. I also made sure the cleaned datasets could be connected through crash IDs and dates.

I used Python and pandas for cleaning. The code is in clean_data.py.&#x20;

## Chicago Crashes

The Crashes dataset contains 222,810 records. Most of the important fields were complete, so I did not remove any crash records.

I found 17 crashes with coordinates recorded as (0, 0), which is not a valid location in Chicago. I changed those coordinates to missing values but kept the crash records. I also added flags for missing coordinates and missing injury information.

There were 509 crashes with missing injury totals. I kept these values missing instead of replacing them with zero because missing information does not mean no injury.

## Chicago People

The People dataset contains 491,892 records.

One person had an age of -59, and 1,965 non-passengers were recorded as age 0. I changed these values to missing but kept the original person records. I kept the 1,109 passengers with age 0 because they could be infants.

I also created age groups for later analysis. I placed people with missing or invalid ages in an "Unknown" age group.

For injury classifications, I created an indicator to distinguish injured and non-injured people. Missing or unrecognized injury classifications were not counted as having no injury.

## NOAA Weather

The original NOAA file contains weather observations from many years. I filtered it to 2023 and 2024, leaving 731 daily observations.

I converted precipitation from tenths of millimeters to millimeters and temperature from tenths of degrees Celsius to degrees Celsius. Snowfall and snow depth were already recorded in millimeters.

## Cleaning Results

| Dataset         | Before Cleaning | After Cleaning |
| --------------- | --------------: | -------------: |
| Chicago Crashes |         222,810 |        222,810 |
| Chicago People  |         491,892 |        491,892 |
| NOAA Weather    |          29,249 |            731 |

The cleaning process kept all crash and person records.

I saved the cleaned datasets separately, so the original files would not be overwritten. 

## Remaining Issues

Some issues cannot be resolved through cleaning alone. For example, 509 crashes have no matching People records, and some crash injury totals do not agree with the person-level records. These values were not changed because there was not enough information to determine which values were correct.

The next step is to integrate the cleaned datasets and check whether the joins work correctly.
