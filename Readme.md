# Music Listening Analytics (Python + SQL)

## Overview
This project analyzes a personal music listening log to understand how listening time varies by **activity context** (workout, studying, relaxing, etc.) and **genre**. The workflow mirrors CRM-style engagement analysis: segment users (activities), compute metrics, and generate reporting outputs.
Most listening time occurred during workouts; rock was the top genre by minutes

## Dataset
Input file: `music.csv`  
Columns:
- date
- artist
- track
- genre
- minutes
- activity

## Workflow
1. **Load & Clean (pandas)**
   - Read CSV into a DataFrame
   - Standardize column names (strip whitespace, lowercase)
   - Standardize text values (trim and normalize activity casing)

2. **Exploratory Checks**
   - Printed `head()` and `info()` to validate schema and types

3. **Engagement Metrics**
   - Computed total listening minutes and activity-level aggregates
   - Aggregated minutes by activity (top activity: **workout = 12 minutes**)
   - Filtered workout rows and sorted by minutes to identify top workout tracks

4. **Deliverables**
   - Exported workout summary to Excel: `workout_summary.xlsx`

5. **Visualization**
   - Genre distribution chart saved as: `minutes_by_genre_pie.png`

6. **SQL Component (SQLite)**
   - Loaded the cleaned dataset into SQLite (`music_log.db`)
   - Queried total minutes by activity using SQL

## Outputs
- `workout_summary.xlsx`
- `minutes_by_genre_pie.png`
- `music_log.db`

# Next Steps
- Add incremental daily logging (append new entries)

## How to Run
```bash
pip install pandas matplotlib openpyxl
python analysis.py





