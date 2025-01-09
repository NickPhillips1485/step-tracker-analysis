# Script for testing that the database schema is correctly setup

import sqlite3

# Connect to the database
conn = sqlite3.connect('step_data.db')
cursor = conn.cursor()

# Check the schema of the steps table
cursor.execute("PRAGMA table_info(steps)")
schema = cursor.fetchall()

# Print the schema
print("Table schema:")
for column in schema:
    print(column)

# Close the connection
conn.close()
