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

def yearly_growth_comparison():
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

    # Query to calculate total miles for each year and compute year-over-year growth
    query = """
        SELECT year, SUM(miles) AS total_miles
        FROM steps
        GROUP BY year
        ORDER BY year;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Convert to a DataFrame
    df = pd.DataFrame(results, columns=['Year', 'Total Miles'])
    df['Yearly Growth'] = df['Total Miles'].diff()  # Calculate year-over-year difference

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(df['Year'], df['Total Miles'], marker='o', label='Total Miles')
    plt.bar(df['Year'], df['Yearly Growth'], alpha=0.6, label='Yearly Growth', color='orange')
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.title('Yearly Growth Comparison', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Miles', fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    yearly_growth_comparison()  # Or replace with yearly_growth_comparison()
    
    # Save the plot as an image
    plt.savefig("yearly_growth_comparison.png")
