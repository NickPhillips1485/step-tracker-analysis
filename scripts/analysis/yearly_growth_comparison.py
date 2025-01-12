import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def yearly_growth_comparison():
    # Connect to the database
    conn = sqlite3.connect(r'C:\Users\nickp\Documents\step-tracker-analysis\step_data.db')
    cursor = conn.cursor()

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
