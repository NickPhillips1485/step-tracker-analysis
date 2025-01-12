# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 12:35:18 2025

@author: nickp
"""

import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def miles_per_month():
    # Connect to the database
    conn = sqlite3.connect(r'C:\Users\nickp\Documents\step-tracker-analysis\step_data.db')
    cursor = conn.cursor()

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
