import requests
import pandas as pd
import json
import csv
import os
import os.path
import pandasql as ps
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

userid = 'beebudda'
week = 0
year = '2024'
last_year_of_contracts = 2028
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

def get_value_from_csv(csv_filepath, key_column, year, value_column):
  """
  Retrieves a value from a CSV file where a specified key matches.

  Args:
    csv_filepath: Path to the CSV file.
    key_column: Name of the column to check for the key.
    key_value: Value to match in the key column.
    value_column: Name of the column containing the desired value.

  Returns:
    The value from the value_column where the key_column matches the key_value, 
    or None if no match is found.
  """
  with open(csv_filepath, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
      if row[key_column] == year:
        return row[value_column]
  return None

# Example usage:
csv_filepath = 'C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\historical_league_info.csv'

def get_value_from_csv(csv_filepath, key_column, year, value_column):
  """
  Retrieves a value from a CSV file where a specified key matches.

  Args:
    csv_filepath: Path to the CSV file.
    key_column: Name of the column to check for the key.
    key_value: Value to match in the key column.
    value_column: Name of the column containing the desired value.

  Returns:
    The value from the value_column where the key_column matches the key_value, 
    or None if no match is found.
  """
  with open(csv_filepath, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
      if row[key_column] == year:
        return row[value_column]
  return None

key_column = 'year'
league_id_column = 'league_id'

leagueid = get_value_from_csv(leagueinfo_filepath, key_column, year, league_id_column)

if leagueid:
  print(f"The value for key '{year}' is: {leagueid}")
else:
  print(f"No record found for key '{year}'.")


def sleeper_transform(funtiontype,userid=None,leagueid=None,week=None,last_year_of_contracts=None):

   if funtiontype == 'matchups':

     #Sleeper Single League matchup Info
      week = []
      for week in range(1, 18):
         print(F"Run for Week {week}")
         new_df = pd.read_csv(f"{funtiontype}_{week}.csv", low_memory=False)
         # Displays the first few rows of the DataFrame
         pd.set_option('display.max_columns', None)
         columns_to_keep = ['player_id', 'fantasy_positions','full_name','status','active','age']
         new_df = new_df[columns_to_keep]
         new_df['fantasy_positions'] = new_df['fantasy_positions'].str.replace(r"\[|\]|\'",'', regex=True).str.strip()
         new_df['full_name'] = new_df['full_name'].str.replace(r"\[|'|\]", '', regex=True).str.strip()
         new_df.to_csv(f"{funtiontype}_{week}.csv", index=False)
         print(f"******** {funtiontype} Start ********")
         print(new_df.head())
         print(f"******** {funtiontype} End********")

         return new_df

   elif funtiontype == 'runplayerdata':

      #Sleeper Single League runplayerdata Info
      new_df = pd.read_csv(f"{funtiontype}.csv", low_memory=False)

      # Displays the first few rows of the DataFrame
      pd.set_option('display.max_columns', None)
      columns_to_keep = ['player_id', 'fantasy_positions','full_name','status','active','age']
      new_df = new_df[columns_to_keep]
      new_df['fantasy_positions'] = new_df['fantasy_positions'].str.replace(r"\[|\]|\'",'', regex=True).str.strip()
      new_df['full_name'] = new_df['full_name'].str.replace(r"\[|'|\]", '', regex=True).str.strip()
      print(f"******** {funtiontype} Start ********")
      print(new_df.head())
      print(f"******** {funtiontype} End********")

      return new_df
      
   elif funtiontype == 'roster':

      #Sleeper Single League Roster Info
      df = pd.read_csv(f"{funtiontype}.csv")

      # Displays the first few rows of the DataFrame
      pd.set_option('display.max_columns', None)
      columns_to_keep = ['league_id','owner_id','players','roster_id']
      new_df = df[columns_to_keep]
      new_df = new_df.rename(columns={'owner_id': 'user_id'})
      new_df = (new_df.assign(player_id=df['players'].str.split(',')).explode(['player_id']))
      new_df['player_id'] = new_df['player_id'].str.replace(r"\[|'|\]", '', regex=True).str.strip()
      new_df.drop('players', axis=1, inplace=True)
      print(f"******** {funtiontype} Start ********")
      print(new_df.head())
      print(f"******** {funtiontype} End ********")

      return new_df

   elif funtiontype == 'allusers':

      #Sleeper Single League Users Info
      df = pd.read_csv(f"{funtiontype}.csv")

      # Displays the first few rows of the DataFrame
      pd.set_option('display.max_columns', None)
      columns_to_keep = ['display_name', 'league_id','user_id','metadata_team_name']
      new_df = df[columns_to_keep]

      print(f"******** {funtiontype} Start ********")
      print(new_df.head())
      print(f"******** {funtiontype} End ********")
      
      return new_df

   elif funtiontype == 'spreadsheet':

      #Sleeper Single League Users Info
      df = pd.read_csv(f"{funtiontype}.csv")

      # Displays the first few rows of the DataFrame
      pd.set_option('display.max_columns', None)
      start_col_name = 'Owner'
      end_col_name = f'{last_year_of_contracts}'
      new_df = df.loc[:, start_col_name:end_col_name]
      #columns_to_keep = ['Owner','Length Remaining','Acquired','Year of Contract','Pos','Player','Per Year $ (In M)','2025','2026','2027','2028']
      #new_df = df[columns_to_keep]
      new_df = new_df.rename(columns={'Year of Contract': 'Year_of_Contract', 'Player': 'full_name', 'Per Year $ (In M)': 'Per_Year_M', 'Length Remaining': 'Length_Remaining'})
      new_df['full_name'] = new_df['full_name'].str.replace(r"\[|'|\]", '', regex=True).str.strip()
      
      print(f"******** {funtiontype} Start ********")
      print(new_df.head())
      print(f"******** {funtiontype} End ********")
      
      return new_df
   
   elif funtiontype == 'transactions' and isinstance(week, int):

      #Sleeper Single League Transactions Info
       
      df = pd.read_csv(f"{funtiontype}_{week}.csv")
      
      # Displays the first few rows of the DataFrame
      pd.set_option('display.max_columns', None)
      columns_to_keep = ['status', 'type','created','creator','draft_picks','transaction_id','consenter_ids','status_updated','settings_waiver_bid','metadata_notes']
      new_df = df[columns_to_keep]
      new_df = new_df.rename(columns={'creator': 'user_id','consenter_ids': 'roster_id_group'})

      print(f"******** {funtiontype} Start ********")
      print(new_df.head())
      print(f"******** {funtiontype} End ********")
            
   elif funtiontype == 'transactions' and week is None:
      print('Please provide week of transaction')

   elif funtiontype == 'transactions' and leagueid is None:
      print('Please provide leagueid')

   elif funtiontype == 'transactions' and week is None and leagueid is None:
      print('Please provide leagueid and week')

      
   elif funtiontype == 'traded_picks':

      #Sleeper Single League Traded Pick Info

      df = pd.read_csv(f"{funtiontype}.csv") 
      # Displays the first few rows of the DataFrame
      pd.set_option('display.max_columns', None)
      new_df = df.rename(columns={'roster_id': 'roster_id_from','owner_id': 'roster_id_to'
                                  ,'previous_owner_id': 'roster_id_org'})

      print(f"******** {funtiontype} Start ********")
      print(new_df.head())
      print(f"******** {funtiontype} End ********")
            
   elif funtiontype == 'traded_picks' and leagueid is None:
      print('Please provide leagueid')
      
#####Sleeper Single League Players #####
roster_df = sleeper_transform(funtiontype='roster',leagueid=leagueid)
runplayerdata_df = sleeper_transform(funtiontype='runplayerdata',leagueid=leagueid)
allusers_df = sleeper_transform(funtiontype='allusers',leagueid=leagueid)
spreadsheet_df = sleeper_transform(funtiontype='spreadsheet',leagueid=leagueid,last_year_of_contracts=last_year_of_contracts)

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

cols_to_keep_spreadsheet_df = spreadsheet_df.loc[:, start_col_name:end_col_name]

print('******** test Start ********')
print(cols_to_keep_spreadsheet_df)
print('******** test end ********')

#spreadsheet_df['full_name'] = spreadsheet_df['full_name'].str.upper()
#merged_df2['full_name'] = merged_df2['full_name'].str.upper()

merged_df3 = merged_df2.merge(cols_to_keep_spreadsheet_df
                            ,on='full_name'
                            ,how='left')

print('******** merged_df3 Start ********')
print(merged_df3.head)
print('******** merged_df3 End ********')

merged_df3.to_csv(f"full_roster.csv", index=False)
