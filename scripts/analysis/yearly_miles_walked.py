import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Use Tkinter-based interactive backend
import sys
import os

# Get the base directory dynamically or use a development fallback
if getattr(sys, 'frozen', False):  # If running as a PyInstaller executable
    base_dir = sys._MEIPASS
else:  # Use the development path during testing
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Dynamically construct the database path
db_path = os.path.join(base_dir, 'step_data.db')

# Uncomment for development if needed
# db_path = r"C:/Users/nickp/Documents/step-tracker-analysis/step_data.db"

def yearly_miles_walked():
    # Connect to the database
    print(f"Database Path: {db_path}")
    conn = sqlite3.connect(db_path)
    query = """
        SELECT year, SUM(miles) AS total_miles
        FROM steps
        GROUP BY year
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['total_miles'], color='skyblue')
    plt.title('Yearly Miles Walked', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Miles Walked', fontsize=12)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    yearly_miles_walked()  # Or replace with yearly_growth_comparison()

  # Save the plot as an image
    plt.savefig("yearly_miles_walked.png")

