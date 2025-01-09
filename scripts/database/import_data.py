
# This script imports step-tracking data from a CSV file


import pandas as pd

# Import the data
data = pd.read_csv(r'C:\Users\nickp\Documents\step-tracker-analysis\source data.csv')

# Preview the data
print(data.head())

# Insert data into the table
for index, row in data.iterrows():
    cursor.execute('INSERT INTO steps (year, month, miles) VALUES (?, ?, ?)', (row['Year'], row['Month'], row['Miles']))

