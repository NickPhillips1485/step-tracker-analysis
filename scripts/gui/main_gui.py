import sys
import os
import matplotlib
matplotlib.use('TkAgg')  # Use Tkinter-based interactive backend
import sqlite3
import sys  

# Get the base directory dynamically or use a development fallback
if getattr(sys, 'frozen', False):  # If running as a PyInstaller executable
    base_dir = sys._MEIPASS
else:  # Use the actual database location
    base_dir = r"C:\Users\nickp\Documents\step-tracker-analysis"

# Dynamically construct the database path
db_path = os.path.join(base_dir, 'step_data.db')

# Get the base directory dynamically
if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Dynamically construct the full file path for the database
db_path = os.path.join(base_dir, 'step_data.db')

# Show Visualisation Function
def show_visualisation(image_path):
    # Open the image
    img = Image.open(image_path)
    img = img.resize((800, 600))  # Resize to fit GUI window

    # Create a new window to display the image
    img_window = tk.Toplevel(root)
    img_window.title("Visualisation")

    canvas = tk.Canvas(img_window, width=800, height=600)
    canvas.pack()

    photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Keep a reference to the image to prevent garbage collection
    img_window.image = photo


# Add the current directory to the search path when packaged
if getattr(sys, 'frozen', False):  # Check if running as an executable
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

sys.path.append(os.path.join(base_path, 'scripts'))

import tkinter as tk
from tkinter import ttk
import sqlite3
from scripts.analysis.yearly_miles_walked import yearly_miles_walked
from scripts.analysis.yearly_growth_comparison import yearly_growth_comparison
from scripts.analysis.miles_walked_per_month import miles_per_month


# Function to query yearly totals
def query_database():
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    elif selected_option == "Visualisation: Yearly Miles Walked":
        yearly_miles_walked()
        show_visualisation("yearly_miles_walked.png")
    elif selected_option == "Visualisation: Yearly Growth Comparison":
        yearly_growth_comparison()
        show_visualisation("yearly_growth_comparison.png")
    elif selected_option == "Visualisation: Miles Walked Per Month":
        miles_per_month()
        show_visualisation("miles_walked_per_month.png")
    else:
        output_box.insert(tk.END, "Invalid query selected.\n")

# Main GUI Logic
root = tk.Tk()
root.title("Step Tracker Analysis")
# (GUI setup continues here)

# Create the main Tkinter window
root = tk.Tk()
root.title("Step Tracker Analysis")

# Add a label
label = tk.Label(root, text="Hi Kip 'The Stepmaster' Phillips! \n Welcome to the Step Tracker Analysis Tool", font=("Arial", 14))
label.pack(pady=10)

# Add a text box to display results
output_box = tk.Text(root, height=30, width=100, font=("Courier New", 12))  # Increased height and width
output_box.pack(pady=10)

# Create a dropdown menu for query selection
options = [
    "View Full Dataset",
    "View Seasonal Trends",
    "Monthly Growth Comparison",
    "View Yearly Totals",
    "View Monthly Trends",
    "Best and Worst Months",
    "Visualisation: Yearly Miles Walked",
    "Visualisation: Yearly Growth Comparison",
    "Visualisation: Miles Walked Per Month"
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
