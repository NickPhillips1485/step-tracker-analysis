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
else:  # Use the actual database location
    base_dir = r"C:\Users\nickp\Documents\step-tracker-analysis"

# Dynamically construct the database path
db_path = os.path.join(base_dir, 'step_data.db')

def miles_per_month():
    # Connect to the database
    print(f"Using database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check the tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)

    if not any('steps' in table for table in tables):
        print("Error: 'steps' table does not exist in the database!")
        return

    # Query to calculate total miles for each month across all years
    query = """
        SELECT month, SUM(miles) AS total_miles
        FROM steps
        GROUP BY month
        ORDER BY 
            CASE month
                WHEN 'January' THEN 1
                WHEN 'February' THEN 2
                WHEN 'March' THEN 3
                WHEN 'April' THEN 4
                WHEN 'May' THEN 5
                WHEN 'June' THEN 6
                WHEN 'July' THEN 7
                WHEN 'August' THEN 8
                WHEN 'September' THEN 9
                WHEN 'October' THEN 10
                WHEN 'November' THEN 11
                WHEN 'December' THEN 12
            END;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Convert to a DataFrame
    df = pd.DataFrame(results, columns=['Month', 'Total Miles'])

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.bar(df['Month'], df['Total Miles'], color='skyblue')
    plt.title('Total Miles Walked Per Month (All Years)', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Miles', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Keep this block for standalone testing
if __name__ == "__main__":
    miles_per_month()
 
    # Save the plot as an image
    plt.savefig("miles_walked_per_month.png")
