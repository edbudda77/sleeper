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

full_roster = pd.read_csv(f"C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\{leaguename}\\Extract\\{year}\\full_roster.csv")

full_roster = full_roster.rename(columns={'2025': 'val_2025','2026': 'val_2026','2027': 'val_2027','2028': 'val_2028'})

managers = """
        SELECT
          distinct Owner
        FROM full_roster
        order by 1 ASC
     """

managers = ps.sqldf(managers, locals())

q1 = """
        SELECT
          Owner
        , Pos
        , player_type
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
          Owner
        , Pos
        , player_type
        , tot_2025
        , tot_2026
        , tot_2027
        , tot_2028
        from (
              SELECT
                Owner
              , Pos
              , player_type
              , sum(case when player_type <> 'TS' then tot_2025
                    else 0 end) as tot_2025
              , sum(case when player_type <> 'TS' then tot_2026
                    else 0 end) as tot_2026
              , sum(case when player_type <> 'TS' then tot_2027
                    else 0 end) as tot_2027
              , sum(case when player_type <> 'TS' then tot_2028
                    else 0 end) as tot_2028
              FROM full_roster
              group by 1,2,3
              union all
              SELECT
                Owner
              , '' as Pos
              , '' as player_type
              , sum(case when player_type <> 'TS' then tot_2025
                    else 0 end) as tot_2025
              , sum(case when player_type <> 'TS' then tot_2026
                    else 0 end) as tot_2026
              , sum(case when player_type <> 'TS' then tot_2027
                    else 0 end) as tot_2027
              , sum(case when player_type <> 'TS' then tot_2028
                    else 0 end) as tot_2028
              FROM full_roster
              group by 1,2,3
        )
        order by 1,2
     """

full_roster = ps.sqldf(q1, locals())
Acq_cost = ps.sqldf(q2, locals())

Acq_cost.to_csv(f"Acq_cost.csv", index=False)

#df = full_roster.query('display_name == "Darkwater59" and Length_Remaining >= 1')

#print(managers)

title("Mo Money Mo Contracts")       

pdf = FPDF()
pdf.set_font("Arial", size=12)

for index, row in managers.iterrows():

   manager = f"{row['Owner']}"

   df = full_roster.query(f'Owner == "{manager}"')

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
   pdf.cell(30, 10, 'Cost Type', 1, 0, 'C')
   pdf.cell(50, 10, 'Player', 1, 0, 'C')
   #pdf.cell(30, 10, 'Per Year $$', 1, 0, 'C')
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
      pdf.cell(20, 10, '%s' % (df['Pos'].iloc[i]), 1, 0, 'C')
      pdf.cell(30, 10, '%s' % (df['player_type'].iloc[i]), 1, 0, 'C')
      pdf.cell(50, 10, '%s' % (df['full_name'].iloc[i]), 1, 0, 'C')
      #pdf.cell(30, 10, '%s' % (df['Per_Year_M'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['tot_2025'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['tot_2026'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['tot_2027'].iloc[i]), 1, 0, 'C')
      pdf.cell(20, 10, '%s' % (df['tot_2028'].iloc[i]), 1, 2, 'C')
      pdf.cell(-260)
   pdf.cell(90, 10, " ", 0, 2, 'C')
   pdf.cell(-30)
   
pdf.output('mmmc.pdf', 'F')
   

