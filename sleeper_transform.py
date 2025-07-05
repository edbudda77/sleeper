import requests
import pandas as pd
import json
import numpy as np
import csv
import os
import os.path
import pandasql as ps
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from get_value_from_csv import get_value_from_csv
from sleeper_build import sleeper_build

userid = 'beebudda'
week = 0
year = '2025'
last_year_of_contracts = '2028'
leaguename = 'mmmc'

# Example usage:
default_folder = f"C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\{leaguename}\\Extract\\{year}"
leagueinfo_filepath = f'C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\{leaguename}\\historical_league_info.csv'
token = 'C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\token.json'
credentials = 'C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\credentials.json'

key_column = 'year'
league_id_column = 'league_id'
draft_id_column = 'draft_id'

# Create output folder
if not os.path.exists(default_folder):
    os.makedirs(default_folder)
    print(f"Folder '{default_folder}' created.")
else:
    print(f"Folder '{default_folder}' already exists.")

# Change the current working directory
os.chdir(default_folder)

# Verify the change
current_directory = os.getcwd()
print("Current working directory:", current_directory)

# Example usage:
csv_filepath = 'C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\historical_league_info.csv'

key_column = 'year'
league_id_column = 'league_id'

leagueid = get_value_from_csv(leagueinfo_filepath, key_column, year, league_id_column)

if leagueid:
  print(f"The value for key '{year}' is: {leagueid}")
else:
  print(f"No record found for key '{year}'.")
      
#####Sleeper Single League Players #####
roster_df = sleeper_build(funtiontype='roster',leagueid=leagueid)
runplayerdata_df = sleeper_build(funtiontype='runplayerdata',leagueid=leagueid)
allusers_df = sleeper_build(funtiontype='allusers',leagueid=leagueid)
spreadsheet_df = sleeper_build(funtiontype='spreadsheet',leagueid=leagueid,last_year_of_contracts=last_year_of_contracts)

spreadsheet_df.to_csv(f"spreadsheet_df.csv", index=False)

filtered_spreadsheet_df = spreadsheet_df[spreadsheet_df['player_type'] == 'Cut']

print('******** filtered_spreadsheet_df Start ********')
print(filtered_spreadsheet_df.head)
print('******** filtered_spreadsheet_df End ********')

cols_to_keep_runplayerdata_df = ['fantasy_positions','full_name','status','active','age','player_id']

merged_df = roster_df.merge(runplayerdata_df[cols_to_keep_runplayerdata_df]
                            ,on='player_id'
                            ,how='left')

print('******** merged_df Start ********')
print(merged_df.head)
print('******** merged_df End ********')

cols_to_keep_allusers_df = ['display_name','metadata_team_name','user_id']

merged_df2 = merged_df.merge(allusers_df[cols_to_keep_allusers_df]
                            ,on='user_id'
                            ,how='left')

print('******** merged_df2 Start ********')
print(merged_df2.head)
print('******** merged_df2 End ********')

start_col_name = 'Owner'
end_col_name = f'{last_year_of_contracts}'

#cols_to_keep_spreadsheet_df = spreadsheet_df.loc[:, start_col_name:end_col_name]
cols_to_keep_spreadsheet_df = spreadsheet_df.loc[:, start_col_name:]

print('******** test Start ********')
print(cols_to_keep_spreadsheet_df)
print('******** test end ********')

#spreadsheet_df['full_name'] = spreadsheet_df['full_name'].str.upper()
#merged_df2['full_name'] = merged_df2['full_name'].str.upper()

merged_df3 = merged_df2.merge(cols_to_keep_spreadsheet_df
                            ,on='full_name'
                            ,how='outer')

merged_df3 = merged_df3.drop([merged_df3.columns[21],merged_df3.columns[22],merged_df3.columns[23],merged_df3.columns[24],merged_df3.columns[25]], axis='columns')

print('******** merged_df3 Start ********')
print(merged_df3.head)
print('******** merged_df3 End ********')

merged_df3.to_csv(f"full_roster.csv", index=False)
