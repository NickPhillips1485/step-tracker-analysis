import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('C:/Users/nickp/Documents/step-tracker-analysis/step_data.db')

# Query for total miles per year
query = "SELECT year, SUM(miles) as total_miles FROM steps GROUP BY year"
data = pd.read_sql_query(query, conn)

conn.close()

print(data)

import matplotlib.pyplot as plt

# Plot Yearly Trends
plt.figure(figsize=(10, 6))
plt.plot(data['year'], data['total_miles'], marker='o', linestyle='-', color='b')
plt.title("Yearly Miles Walked", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Total Miles", fontsize=14)
plt.grid(True)
plt.show()


