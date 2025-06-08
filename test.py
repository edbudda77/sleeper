import pandas as pd
import matplotlib
import pandasql as ps
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF

year = 2025

full_roster = pd.read_csv(f"C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\Extract\\{year}\\full_roster.csv")

full_roster = full_roster.rename(columns={'2025': 'val_2025','2026': 'val_2026','2027': 'val_2027','2028': 'val_2028'})

managers = """
        SELECT
          distinct display_name
        FROM full_roster
     """

managers = ps.sqldf(managers, locals())

q1 = """
        SELECT
          display_name
        , fantasy_positions
        , Length_Remaining
        , Acquired
        , Year_of_Contract
        , full_name
        , CAST(REPLACE(Per_Year_M, '$', '') AS DECIMAL(18,3)) as Per_Year_M
        , sum(CAST(REPLACE(val_2025, '$', '') AS DECIMAL(18,3))) as tot_2025
        , sum(CAST(REPLACE(val_2026, '$', '') AS DECIMAL(18,3))) as tot_2026
        , sum(CAST(REPLACE(val_2027, '$', '') AS DECIMAL(18,3))) as tot_2027
        , sum(CAST(REPLACE(val_2028, '$', '') AS DECIMAL(18,3))) as tot_2028
        FROM full_roster
        group by 1,2,3,4,5,6,7
     """

q2 = """
        SELECT
          fantasy_positions
        , SUBSTR(Acquired, 1, INSTR(Acquired, '-') - 1) as Acquired_type
        , full_name
        , Per_Year_M
        , sum(tot_2025) as tot_2025
        , sum(tot_2026) as tot_2026
        , sum(tot_2027) as tot_2027
        , sum(tot_2028) as tot_2028
        FROM full_roster
        group by 1,2,3
     """

full_roster = ps.sqldf(q1, locals())
Acq_cost = ps.sqldf(q2, locals())

#df = full_roster.query('display_name == "Darkwater59" and Length_Remaining >= 1')

#print(managers)

title("Mo Money Mo Contracts")       

pdf = FPDF()
pdf.set_font("Arial", size=12)

for index, row in managers.iterrows():

   manager = f"{row['display_name']}"

   df = full_roster.query(f'display_name == "{manager}" and Length_Remaining >= 1')

   pdf.add_page(orientation = 'L')
   pdf.set_xy(0, 0)
   pdf.set_font('arial', 'B', 15)
   pdf.cell(60)
   pdf.cell(0, 10, f"{manager}", 0, 2, 'C')
   pdf.set_font('arial', 'B', 12)
   pdf.cell(90, 10, " ", 0, 2, 'C')
   pdf.cell(-50)
   #pdf.cell(40, 10, 'Manager', 1, 0, 'C')
   pdf.cell(50, 10, 'Years Remaining', 1, 0, 'C')
   pdf.cell(30, 10, 'Acquired', 1, 0, 'C')
   pdf.cell(20, 10, 'Year', 1, 0, 'C')
   pdf.cell(20, 10, 'Pos', 1, 0, 'C')
   pdf.cell(50, 10, 'Player', 1, 0, 'C')
   pdf.cell(30, 10, 'Per Year $$', 1, 0, 'C')
   pdf.cell(20, 10, '2025', 1, 0, 'C')
   pdf.cell(20, 10, '2026', 1, 0, 'C')
   pdf.cell(20, 10, '2027', 1, 0, 'C')
   pdf.cell(20, 10, '2028', 1, 2, 'C')
   pdf.cell(-260)
   pdf.set_font('arial', '', 12)
   for i in range(0, len(df)):
   #   pdf.cell(40, 10, '%s' % (df['display_name'].iloc[i]), 1, 0, 'C')
      pdf.cell(50, 10, '%s' % (df['Length_Remaining'].iloc[i]), 1, 0, 'C')
      pdf.cell(30, 10, '%s' % (df['Acquired'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['Year_of_Contract'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['fantasy_positions'].iloc[i]), 1, 0, 'C')
      pdf.cell(50, 10, '%s' % (df['full_name'].iloc[i]), 1, 0, 'C')
      pdf.cell(30, 10, '%s' % (df['Per_Year_M'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['tot_2025'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['tot_2026'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['tot_2027'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['tot_2028'].iloc[i]), 1, 2, 'C')
      pdf.cell(-260)
   pdf.cell(90, 10, " ", 0, 2, 'C')
   pdf.cell(-30)
   
pdf.output('test.pdf', 'F')
   

