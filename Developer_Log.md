# Developer Log: Step Tracker Analysis

## Overview
This document tracks the progress and challenges of the Step Tracker Analysis project.

I have been learning:
- SQL (intermediate level, 6 months).
- Python (beginner level, 2 months).
- GitBash and GitHub (reasonable proficiency).

This project combines these skills into a practical application with support from ChatGPT.

### Project Basis
For the past six years (2019–2024 inclusive), my dad has been tracking his daily steps. I recorded this data in a spreadsheet, broken down by month. This dataset is simple yet meaningful and serves as the foundation for building:
1. An SQL database.
2. A GUI for easy query execution.
3. Data visualisations.

---

## Preparing the Dataset
To keep the dataset straightforward:
- I decided on three columns: **Year**, **Month**, and **Miles**.
- I saved the data as a `.csv` file.

---

## Setting up the GitHub Repository

### Git Setup
In GitBash:

```
# Check Git installation
git --version
# Output: git version 2.47.0.windows.1

# Configure user details
git config --global user.name "Redacted"
git config --global user.email "Redacted"

# Create main project directory
mkdir step-tracker-analysis
cd step-tracker-analysis

# Create subfolders
mkdir data scripts visualisations tests docs
mkdir scripts/database scripts/gui scripts/analysis

# Stage all changes
git add .

# Commit the changes
git commit -m "Set up initial folder structure"

# Attempt to push changes
git push origin main

nothing to commit, working tree clean

# Add .gitkeep files to each folder
touch data/.gitkeep
touch scripts/.gitkeep
touch scripts/database/.gitkeep
touch scripts/gui/.gitkeep
touch scripts/analysis/.gitkeep
touch visualisations/.gitkeep
touch tests/.gitkeep
touch docs/.gitkeep

# Stage and commit again
git add .
git commit -m "Add .gitkeep files to track empty folders"
git push origin main```

## Database Setup

Created the SQLite Database:

Wrote a create_database.py script to create an SQLite database (step_data.db) and a table (steps) with the schema:
year (INTEGER)
month (TEXT)
miles (REAL)
Resolved Table Schema Issues:

Initial attempts resulted in a malformed schema ('INTEGER\n month TEXT\n miles REAL' due to formatting issues).
Fix: Simplified the SQL CREATE TABLE statement to a single line, ensuring SQLite correctly interpreted the schema.

## Importing Data

Wrote the import_data.py Script:

Loaded Source Data.csv into a pandas DataFrame.
Inserted the data row-by-row into the steps table.
Verified that the data was successfully inserted using:

```
SELECT * FROM steps LIMIT 5;
```

Challenges & Fixes

Encountered issues with column names (KeyError: 'Year') due to mismatched column headers in the CSV.
Updated the CSV to ensure headers matched (Year, Month, Miles).
Successfully re-imported the data.

## Querying the database

Test Query:
Wrote a test script to query total miles walked per year:

```
SELECT year, SUM(miles) FROM steps GROUP BY year;
```

Verified the results, which displayed yearly totals.