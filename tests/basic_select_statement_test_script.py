

import sqlite3

# Connect to the database
conn = sqlite3.connect('C:/Users/nickp/Documents/step-tracker-analysis/step_data.db')
cursor = conn.cursor()

# Query the first 10 rows from the steps table
cursor.execute("SELECT * FROM steps LIMIT 10")
rows = cursor.fetchall()

# Print the results
print("Data in 'steps' table:")
for row in rows:
    print(row)

# Close the connection
conn.close()
