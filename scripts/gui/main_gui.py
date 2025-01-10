import tkinter as tk
from tkinter import ttk
import sqlite3

# Function to query yearly totals
def query_database():
    conn = sqlite3.connect('C:/Users/nickp/Documents/step-tracker-analysis/step_data.db')
    cursor = conn.cursor()
    query = "SELECT year, SUM(miles) AS total_miles FROM steps GROUP BY year"
    cursor.execute(query)
    results = cursor.fetchall()
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Yearly Totals:\n\n")
    for row in results:
        output_box.insert(tk.END, f"Year: {row[0]}, Total Miles: {row[1]:.2f}\n")
    conn.close()

# Function to query and display monthly trends
def query_monthly_trends():
    conn = sqlite3.connect('C:/Users/nickp/Documents/step-tracker-analysis/step_data.db')
    cursor = conn.cursor()
    query = """
    SELECT month, AVG(miles) AS avg_miles
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
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Monthly Trends (Average Miles):\n\n")
    for row in results:
        output_box.insert(tk.END, f"Month: {row[0]}, Avg Miles: {row[1]:.2f}\n")
    conn.close()

# Function to query and display seasonal trends
def query_seasonal_trends():
    conn = sqlite3.connect('C:/Users/nickp/Documents/step-tracker-analysis/step_data.db')
    cursor = conn.cursor()
    query = """
    SELECT 
        CASE 
            WHEN month IN ('December', 'January', 'February') THEN 'Winter'
            WHEN month IN ('March', 'April', 'May') THEN 'Spring'
            WHEN month IN ('June', 'July', 'August') THEN 'Summer'
            WHEN month IN ('September', 'October', 'November') THEN 'Autumn'
        END AS season,
        AVG(miles) AS avg_miles
    FROM steps
    GROUP BY season
    ORDER BY 
        CASE season
            WHEN 'Winter' THEN 1
            WHEN 'Spring' THEN 2
            WHEN 'Summer' THEN 3
            WHEN 'Autumn' THEN 4
        END;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Seasonal Trends (Average Miles):\n\n")
    for row in results:
        output_box.insert(tk.END, f"Season: {row[0]}, Avg Miles: {row[1]:.2f}\n")
    conn.close()

# Function to display monthly growth comparison
def query_monthly_growth():
    conn = sqlite3.connect('C:/Users/nickp/Documents/step-tracker-analysis/step_data.db')
    cursor = conn.cursor()

    query = """
    SELECT year, month, miles,
           LAG(miles) OVER (PARTITION BY month ORDER BY year) AS prev_year_miles,
           (miles - LAG(miles) OVER (PARTITION BY month ORDER BY year)) AS growth
    FROM steps
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
        END, year;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Monthly Growth Comparison:\n\n")

    current_month = None
    for row in results:
        year, month, miles, prev_year_miles, growth = row
        if month != current_month:
            if current_month is not None:
                output_box.insert(tk.END, "\n")  # Add space between months
            current_month = month
        growth_display = f"{growth:+.2f}" if growth is not None else "N/A"
        output_box.insert(
            tk.END, f"Year: {year}, Month: {month}, Miles: {miles:.2f}, Growth: {growth_display}\n"
        )
    conn.close()

# Function to display best and worst months
def query_best_and_worst_months():
    conn = sqlite3.connect('C:/Users/nickp/Documents/step-tracker-analysis/step_data.db')
    cursor = conn.cursor()

    # Best and Worst Months for Each Year
    query_yearly = """
    SELECT year, MAX(miles) AS max_miles, MIN(miles) AS min_miles
    FROM steps
    GROUP BY year
    """
    cursor.execute(query_yearly)
    yearly_results = cursor.fetchall()

    # Overall Best and Worst Months
    query_best = """
    SELECT year, month, MAX(miles) AS max_miles
    FROM steps
    WHERE miles = (SELECT MAX(miles) FROM steps)
    """
    cursor.execute(query_best)
    best = cursor.fetchone()

    query_worst = """
    SELECT year, month, MIN(miles) AS min_miles
    FROM steps
    WHERE miles = (SELECT MIN(miles) FROM steps)
    """
    cursor.execute(query_worst)
    worst = cursor.fetchone()

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Best and Worst Months:\n\n")
    output_box.insert(tk.END, "Yearly Best and Worst Months:\n")
    for row in yearly_results:
        output_box.insert(tk.END, f"Year: {row[0]}, Max Miles: {row[1]:.2f}, Min Miles: {row[2]:.2f}\n")
    output_box.insert(tk.END, "\nOverall Best and Worst Months:\n")
    output_box.insert(tk.END, f"Best Month: {best[1]} {best[0]} with {best[2]:.2f} miles\n")
    output_box.insert(tk.END, f"Worst Month: {worst[1]} {worst[0]} with {worst[2]:.2f} miles\n")
    conn.close()

# Function to display full dataset
def query_full_dataset():
    conn = sqlite3.connect('C:/Users/nickp/Documents/step-tracker-analysis/step_data.db')
    cursor = conn.cursor()

    query = """
    SELECT year, month, miles
    FROM steps
    ORDER BY year,
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

    year_totals = {}
    overall_total = 0
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Full Dataset:\n\nYear\tMonth\tMiles\n")
    output_box.insert(tk.END, "-" * 30 + "\n")

    current_year = None
    for row in results:
        year, month, miles = row
        if year != current_year:
            if current_year is not None:
                output_box.insert(tk.END, f"Total for {current_year}: {year_totals[current_year]:.2f}\n\n")
            current_year = year
        year_totals[year] = year_totals.get(year, 0) + miles
        overall_total += miles
        output_box.insert(tk.END, f"{year}\t{month}\t{miles:.2f}\n")

    if current_year is not None:
        output_box.insert(tk.END, f"Total for {current_year}: {year_totals[current_year]:.2f}\n\n")
    output_box.insert(tk.END, f"Combined Total for All Years: {overall_total:.2f}\n")
    conn.close()

# Function to handle dropdown query selection
def handle_query(selected_option):
    if selected_option == "View Full Dataset":
        query_full_dataset()
    elif selected_option == "View Seasonal Trends":
        query_seasonal_trends()
    elif selected_option == "Monthly Growth Comparison":
        query_monthly_growth()
    elif selected_option == "View Yearly Totals":
        query_database()
    elif selected_option == "View Monthly Trends":
        query_monthly_trends()
    elif selected_option == "Best and Worst Months":
        query_best_and_worst_months()

# Create the main Tkinter window
root = tk.Tk()
root.title("Step Tracker Analysis")

# Add a label
label = tk.Label(root, text="Hi Kip 'The Stepmaster' Phillips! \n Welcome to the Step Tracker Analysis Tool", font=("Arial", 14))
label.pack(pady=10)

# Add a text box to display results
output_box = tk.Text(root, height=20, width=70, font=("Courier New", 12))
output_box.pack(pady=10)

# Create a dropdown menu for query selection
options = [
    "View Full Dataset",
    "View Seasonal Trends",
    "Monthly Growth Comparison",
    "View Yearly Totals",
    "View Monthly Trends",
    "Best and Worst Months"
]
selected_query = tk.StringVar(root)
selected_query.set(options[0])  # Set default value

dropdown = tk.OptionMenu(root, selected_query, *options)
dropdown.config(font=("Arial", 12))
dropdown.pack(pady=5)

# Add a button to execute the selected query
execute_button = tk.Button(root, text="Run Query", command=lambda: handle_query(selected_query.get()), font=("Arial", 12))
execute_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
