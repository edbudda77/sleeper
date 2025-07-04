import pandas as pd
import matplotlib
import pandasql as ps
import os
import os.path
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF

year = 2025
leaguename = 'mmmc'

default_folder = f"C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\{leaguename}\\Extract\\{year}"

# Change the current working directory
os.chdir(default_folder)

# Verify the change
current_directory = os.getcwd()
print("Current working directory:", current_directory)
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "", 10)

data = [
        {"Name": "Alice", "Status": "Active"},
        {"Name": "Bob", "Status": "Inactive"},
        {"Name": "Charlie", "Status": "Inactive"},
]

for row_data in data:
# Check the value that determines the color
   if row_data["Status"] == "Active":
      pdf.set_fill_color(193, 229, 252)  # Light blue for Active
   else:
      pdf.set_fill_color(255, 204, 204)  # Light red for Inactive

        # Draw each cell in the row with the determined fill color
pdf.cell(40, 10, row_data["Name"], 1, 0, "L", 1)  # Last '1' enables fill
pdf.cell(40, 10, row_data["Status"], 1, 0, "L", 1)
pdf.ln()  # Move to the next line for the next row

pdf.output('test.pdf', 'F')
   
