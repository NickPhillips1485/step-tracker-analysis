
# This script imports step-tracking data from a CSV file into the SQLite database

import pandas as pd
import sqlite3

# Import the data from the CSV file
data = pd.read_csv(r'C:\Users\nickp\Documents\step-tracker-analysis\Source Data.csv')

# Preview the data
print("Preview of the data:")
print(data.head())

# Connect to the SQLite database
conn = sqlite3.connect(r'C:\Users\nickp\Documents\step-tracker-analysis\step_data.db')
cursor = conn.cursor()

# Insert data into the steps table
print("Inserting data into the database...")
for index, row in data.iterrows():
    cursor.execute(
        'INSERT INTO steps (year, month, miles) VALUES (?, ?, ?)',
        (row['Year'], row['Month'], row['Miles'])
    )

# Commit the changes and close the connection
conn.commit()
conn.close()
print("Data insertion complete.")

