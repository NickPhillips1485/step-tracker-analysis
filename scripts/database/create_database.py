
import sqlite3

# Creating the database
conn = sqlite3.connect('step_data.db')

# Creating cursor object to run SQL commands
cursor = conn.cursor()

# Drop the table if it exists (to ensure clean creation)
cursor.execute("DROP TABLE IF EXISTS steps")

# Creating table (as a single line to avoid formatting issues)
cursor.execute("CREATE TABLE IF NOT EXISTS steps (year INTEGER, month TEXT, miles REAL)")

# Committing changes and closing the connection
conn.commit()
conn.close()

print("Table recreated successfully.")






