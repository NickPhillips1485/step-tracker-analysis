# Test Query - Total Miles Per Year

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/nickp/Documents/step-tracker-analysis/step_data.db')
cursor = conn.cursor()

# Execute the SQL query to group by year and sum miles
cursor.execute("SELECT year, SUM(miles) FROM steps GROUP BY year")
rows = cursor.fetchall()

# Print the results
print("Yearly Total Miles:")
for row in rows:
    print(f"Year: {row[0]}, Total Miles: {row[1]}")

# Close the connection
conn.close()
