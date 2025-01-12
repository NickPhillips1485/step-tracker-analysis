import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def yearly_miles_walked():
    # Connect to the database
    conn = sqlite3.connect(r'C:\Users\nickp\Documents\step-tracker-analysis\step_data.db')
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


