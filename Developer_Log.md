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
git push origin main
```

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

SELECT * FROM steps LIMIT 5;

Challenges & Fixes

Encountered issues with column names (KeyError: 'Year') due to mismatched column headers in the CSV.
Updated the CSV to ensure headers matched (Year, Month, Miles).
Successfully re-imported the data.

## Querying the database

Test Query:
Wrote a test script to query total miles walked per year:

SELECT year, SUM(miles) FROM steps GROUP BY year;

Verified the results, which displayed yearly totals.

## Building the GUI

I will say at the outset that the code for the GUI was written by ChatGPT. I have no experience of using `tkinter`, so I used this as a learning opportunity. I reviewed the code thoroughly afterwards, and although I could not yet write it myself, I am starting to get to grips with some of the concepts—such as adding buttons, labels, and dropdown menus.

In a nutshell, the structure of the `main_gui.py` file is as follows: 
- After importing `tkinter`, separate SQL blocks are written for each of the query options (e.g., Seasonal Trends, Best & Worst Months, etc.).
- The GUI is then defined using components such as dropdowns, buttons, labels, and a text box to display the output.

It was useful that each time the code was tweaked, I was able to view the latest version of the GUI by running the script in Spyder. This iterative approach allowed me to see immediate results and understand how the changes impacted the interface.

### Challenges
The code had to go through multiple iterations as some of the queries would not display in the GUI due to `NameError` exceptions. We found ourselves in a cycle whereby fixing errors for some of the queries would inadvertently break others. Eventually, this was resolved, and ChatGPT explained the root of the issue as follows:

> "The issue stemmed from inconsistent inclusion and integration of functions across iterations of the script, including missing functions, conflicts between function names, overwriting of code, and fragmented debugging."

While this was a frustrating challenge, it highlighted the importance of maintaining a structured and systematic approach to coding, especially when integrating multiple components into a single file.

## Creating the executable

Next, I wanted to understand the process for:

a) Creating a desktop shortcut for running the GUI, rather than having to call it from the Anaconda Prompt.
b) Packaging up the application so it could be installed and used on my dad's laptop.

Step 1: Installing PyInstaller
To begin, I needed a tool to convert my Python script into an executable file. I chose PyInstaller for this purpose. First, I installed it using the following command:

```pip install pyinstaller```

Step 2: Generating the Executable
After installing PyInstaller, I navigated to the directory containing the main_gui.py file. From the Anaconda Prompt, I ran the following command:

```pyinstaller --onefile main_gui.py```

This command does the following:

Converts the Python script (main_gui.py) into a standalone executable file.
The --onefile flag ensures that the output is a single .exe file, rather than multiple files.

Step 3: Locating the Output
Once the process completed, PyInstaller created a dist folder within the current directory. This folder contained the generated executable file: main_gui.exe.

Step 4: Testing the Executable
To ensure the executable worked as intended, I double-clicked the main_gui.exe file. The GUI opened successfully, and I was able to interact with it without needing to run Python or Anaconda.

Step 5: Creating a Desktop Shortcut
To make the executable more accessible:

I right-clicked on the main_gui.exe file and selected Create Shortcut.
I moved the shortcut to my desktop for easy access.

Step 6: Addressing Antivirus Issues
Initially, my antivirus software (Norton) flagged the executable as a potential threat (Win64:Malware-gen) and quarantined it. After some investigation, I discovered this is a common issue with executables generated by PyInstaller. To resolve this:

I restored the file from quarantine.
I added the file to Norton’s exclusion list to prevent further false positives.

Step 7: Preparing for Installation on Another Machine
Finally, I explored how to package the executable for installation on another machine (e.g., my dad's laptop). To do this, he'll need the main_gui.exe file and the step_data.db file on his machine.
According to ChatGPT, in future I should also consider bundling the application into a proper installer using tools like Inno Setup or NSIS for a more polished experience.

## Adding Visualisations

A key enhancement to the application was the introduction of visualisations. Three distinct visualisation types were developed:

Yearly Miles Walked: A bar chart representing the total miles walked per year.

Yearly Growth Comparison: A combined line and bar chart displaying total miles per year and the year-over-year growth.

Miles Walked Per Month: A bar chart showing the total miles walked for each month, aggregated across all years.

These visualisations were implemented as standalone Python scripts, ensuring modularity and ease of testing. The scripts were called dynamically from the main GUI, and a dedicated function was created to display the visualisation in a Tkinter popup window.

Transition to a New Release

The addition of visualisations and the changes this entailed effectively meant a new release. This led to the following tasks:

Updating the database path resolution logic - these could not be hardcoded or I would not be able to deploy the application on my dad's laptop. 

Rebuilding the executable to include the new features and dependencies.

Addressing the Database Path Issue

Previously, the database path was hardcoded in various scripts, which created challenges when transitioning the application to a new system. To resolve this, we implemented a dynamic database path resolution mechanism:

We used os.path.dirname and os.path.abspath to locate the directory of the executable or script.

If running as a PyInstaller executable, sys._MEIPASS was used to resolve the base directory.

All instances of the hardcoded database path were replaced with this dynamically constructed db_path variable.

Debugging included adding print statements to confirm the correct database file was being accessed.

## Rebuilding the Executable

The executable needed to be rebuilt with these changes, as well as additional dependencies to ensure smooth functionality:

Updated PyInstaller Command:

```pyinstaller --onefile --add-data "C:/Users/nickp/Documents/step-tracker-analysis/step_data.db;." --add-data "C:/Users/nickp/Documents/step-tracker-analysis/scripts;scripts" --hidden-import=pandas --hidden-import=pandas._libs.tslibs main_gui.py```

Added pandas and its submodules explicitly as hidden imports to resolve runtime issues.

Included the database and scripts directory using --add-data.

Challenges Overcome:

Memory errors during the build process were addressed by running PyInstaller in --exclude-module mode to streamline dependencies.

Specific inclusion of problematic modules like pandas resolved issues with importing during runtime.

Verification:

The new executable was thoroughly tested to ensure it could locate the database and render visualisations correctly.

### Preparing the Application for Distribution

To ensure portability:

The dist/main_gui.exe file and step_data.db were packaged together into a ZIP file.

Clear instructions were provided to extract both files into the same directory on the target system.

### Handling Antivirus Warnings

On the target system, Norton Antivirus flagged the download as suspicious. This was resolved by:

Using Norton’s interface to whitelist the download site and file.

Re-attempting the download after confirming the integrity of the ZIP file.

### Final Installation

The application was successfully installed on the target laptop:

Extracting the ZIP file placed both the executable and database in the same folder.

The application launched successfully, and all functionalities, including visualisations, worked as expected.

### Resolving GitHub Repository Issues

During the final stages, we encountered issues with pushing changes to the GitHub repository due to large files being included in previous commits. These files exceeded GitHub's maximum file size limits and needed to be removed from the repository history.

Challenges:

Large files like main_gui.exe and other build artifacts were previously committed, causing the push to fail.

Adjusting the .gitignore file did not resolve the issue, as the files were already part of the repository's history.

Solution:

To clean up the repository and remove the large files:

Installed the BFG Repo-Cleaner (Java had to be installed for this to work), a tool for removing large files and sensitive data from Git history.

Ran the following command in cmd to strip large files:

```java -jar bfg-1.14.0.jar --strip-blobs-bigger-than 100M .git```

Followed up with a Git garbage collection to clean up unnecessary data:

```git reflog expire --expire=now --all```
```git gc --prune=now --aggressive```

In Bash, forced the cleaned repository to be pushed back to GitHub:

```git push origin main --force```


Outcome:

The repository was successfully updated with a clean history, and large files are now properly excluded by .gitignore. The Developer Log and all necessary code changes are now pushed to GitHub.
The lesson here is to properly set up the .gitignore at the outset to ensure these large file types are not included (unless they are absolutely critical to the repository).