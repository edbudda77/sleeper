import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import numpy as np
import json
import csv
import os
import sys
import csv
import os.path
import shutil
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1cVkswp7NckK7kxG0sb1m7qH8siA0dtgFZ6p8zorXimg"
SAMPLE_RANGE_NAME = "Player Contracts!A5:P"

userid = 'beebudda'
year = '2025'
leaguename = 'mmmc'

def copy_file(source_path, destination_dir):
    """Copies a file to a specified directory.

    Args:
        source_path: The path to the file to be copied.
        destination_dir: The directory to copy the file to.
    """
    try:
        shutil.copy(source_path, destination_dir)
        print(f"File '{source_path}' copied successfully to '{destination_dir}'")
    except FileNotFoundError:
        print(f"Error: File '{source_path}' not found.")
    except PermissionError:
      print(f"Error: Permission denied to access '{source_path}' or '{destination_dir}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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
leagueinfo_filepath = f'C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\{leaguename}\\historical_league_info.csv'
token = 'C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\token.json'
credentials = 'C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\credentials.json'

key_column = 'year'
league_id_column = 'league_id'
draft_id_column = 'draft_id'

leagueid = get_value_from_csv(leagueinfo_filepath, key_column, year, league_id_column)

if leagueid:
  print(f"The leagueid for '{year}' is: {leagueid}")
else:
  print(f"No leagueid record found for key '{year}'.")

draftid = get_value_from_csv(leagueinfo_filepath, key_column, year, draft_id_column)

if draftid:
  print(f"The draftid for '{year}' is: {draftid}")
else:
  print(f"No draftid record found for key '{year}'.")
    
default_folder = f"C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\{leaguename}\\Extract\\{year}"

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

# Copy token to year directory
copy_file(token, default_folder)
# Copy credentials to year directory
copy_file(credentials, default_folder)

def sleeper_data(funtiontype,userid=None,leagueid=None,week=None,draftid=None):

   if funtiontype == 'runplayerdata':
        
      #Sleeper pull player data
      filename = f"{funtiontype}.json"
      df = requests.get('https://api.sleeper.app/v1/players/nfl')
      dfjson = df.json()
      with open(filename, "w") as f:
         json.dump(dfjson, f, indent=3)
      # Use pd.json_normalize to convert the JSON to a DataFrame
      dframe = [*dfjson.values()]
      dframe = pd.json_normalize(dframe, max_level=1)
      dframe.to_csv(f"{funtiontype}.csv", index=False)
      print(F'{funtiontype} info out')

   elif funtiontype == 'draft':
    
      #Sleeper draft Info
       
      filename = f"{funtiontype}.json"
      df = requests.get(f'https://api.sleeper.app/v1/draft/{draftid}/picks')
      dfjson = df.json()
      with open(filename, "w") as f:
         json.dump(dfjson, f, indent=1)
      # Use pd.json_normalize to convert the JSON to a DataFrame
      dframe = pd.json_normalize(dfjson, max_level=1)
      dframe.to_csv(f"{funtiontype}.csv", index=False)
      print(F'{funtiontype} info out')
      
   elif funtiontype == 'user' and isinstance(userid, str):
    
      #Sleeper User Info
       
      filename = f"{funtiontype}_{userid}.json"
      df = requests.get(f'https://api.sleeper.app/v1/user/{userid}')
      dfjson = df.json()
      with open(filename, "w") as f:
         json.dump(dfjson, f, indent=1)
      # Use pd.json_normalize to convert the JSON to a DataFrame
      dframe = pd.json_normalize(dfjson, max_level=1)
      dframe.to_csv(f"{funtiontype}_{userid}.csv", index=False)
      print(F'{funtiontype} info for {userid} out')

   elif funtiontype == 'user' and userid is None: print(f'Plese provide user')
       
   elif funtiontype == 'league' and isinstance(leagueid, str):    
    
      #Sleeper Single League Info

      print(F'{funtiontype} Id is: {leagueid}')
       
      filename = f"{funtiontype}.json"
      df = requests.get(f'https://api.sleeper.app/v1/league/{leagueid}')
      dfjson = df.json()
      with open(filename, "w") as f:
         json.dump(dfjson, f, indent=1)
      # Use pd.json_normalize to convert the JSON to a DataFrame
      dframe = pd.json_normalize(dfjson, max_level=1)
      dframe.columns = dframe.columns.str.replace('.', '_')
      dframe.to_csv(f"{funtiontype}.csv", index=False)
      print(F'{funtiontype} info out')

   elif funtiontype == 'league' and leagueid is None: print(f'Plese provide league ID')
   
   elif funtiontype == 'roster' and isinstance(leagueid, str):

      #Sleeper Single League Roster Info
      filename = f"{funtiontype}.json"
      df = requests.get(f'https://api.sleeper.app/v1/league/{leagueid}/rosters')
      dfjson = df.json()
      with open(filename, "w") as f:
         json.dump(dfjson, f, indent=1)
      dframe = pd.json_normalize(dfjson, max_level=1)
      dframe.columns = dframe.columns.str.replace('.', '_')
      dframe.to_csv(f"{funtiontype}.csv", index=False)
      print(F'{funtiontype} info out')

   elif funtiontype == 'allusers':

      #Sleeper Single League Users Info
      filename = f"{funtiontype}.json"
      df = requests.get(f'https://api.sleeper.app/v1/league/{leagueid}/users')
      dfjson = df.json()
      with open(filename, "w") as f:
         json.dump(dfjson, f, indent=1)
      dframe = pd.json_normalize(dfjson, max_level=1)
      dframe.columns = dframe.columns.str.replace('.', '_')
      dframe.to_csv(f"{funtiontype}.csv", index=False)
      print(F'{funtiontype} info out')

   elif funtiontype == 'transactions':

      #Sleeper Single League Transactions Info
      week = []
      for week in range(1, 18):
         print(F"Transactions for Week {week}")     
         filename = f"{funtiontype}_{week}.json"
         df = requests.get(f'https://api.sleeper.app/v1/league/{leagueid}/{funtiontype}/{week}')
         dfjson = df.json()
         with open(filename, "w") as f:
            json.dump(dfjson, f, indent=1)
         dframe = pd.json_normalize(dfjson, max_level=1)
         dframe.columns = dframe.columns.str.replace('.', '_')
         dframe.to_csv(f"{funtiontype}_{week}.csv", index=False)
         print(F'{funtiontype} for week {week} info out')


   elif funtiontype == 'transactions' and leagueid is None:
      print('Please provide leagueid')

   elif funtiontype == 'matchups':

      #Sleeper Single League matchup Info
      week = []
      for week in range(1, 18):
         print(F"Run for Week {week}")
         filename = f"{funtiontype}_{week}.json"
         df = requests.get(f'https://api.sleeper.app/v1/league/{leagueid}/{funtiontype}/{week}')
         dfjson = df.json()
         with open(filename, "w") as f:
            json.dump(dfjson, f, indent=1)
         dframe = pd.json_normalize(dfjson, max_level=2)
         #players_points         
         columns_to_keep = ['roster_id','matchup_id','starters','players']
         prefix = 'players_points_'
         dframe.columns = dframe.columns.str.replace('.', '_')
         playerout = dframe.filter(like=prefix)
         playerout.columns = playerout.columns.str.removeprefix('players_points_')
         #pull player IDs
         playerout_id = playerout[playerout.notna().all(axis=1)].T.reset_index()
         playerout_id.columns = ['player_id']
         playerout_id['key'] = range(1, len(playerout_id) + 1)
         #pull player points
         playerout_pts = playerout.select_dtypes(include='number').sum().to_frame(name='player_score')
         playerout_pts['key'] = range(1, len(playerout_pts) + 1)
         dframe = dframe[columns_to_keep]
         dframe.to_csv(f"{funtiontype}_{week}.csv", index=False)
         cols_to_keep = ['player_score','key']
         playerout_score = playerout_id.merge(playerout_pts[cols_to_keep]
                            ,on='key'
                            ,how='left').drop('key', axis=1)
         playerout_score.to_csv(f"{funtiontype}_playerout_score_{week}.csv", index=False)
         print(F'{funtiontype} for week {week} info out')

   elif funtiontype == 'matchups' and leagueid is None:
      print('Please provide leagueid')

      
   elif funtiontype == 'traded_picks':

      #Sleeper Single League Traded Pick Info

      filename = f"{funtiontype}.json" 
      df = requests.get(f'https://api.sleeper.app/v1/league/{leagueid}/{funtiontype}')
      dfjson = df.json()
      with open(filename, "w") as f:
         json.dump(dfjson, f, indent=1)
      dframe = pd.json_normalize(dfjson, max_level=1)
      dframe.columns = dframe.columns.str.replace('.', '_')
      dframe.to_csv(f"{funtiontype}.csv", index=False)
      print(F'{funtiontype} info out')

   elif funtiontype == 'traded_picks' and leagueid is None:
       
      print('Please provide leagueid')

   elif funtiontype == 'spread_sheet':
       
      """Shows basic usage of the Sheets API.
      Prints values from a sample spreadsheet.
      """
      creds = None
      # The file token.json stores the user's access and refresh tokens, and is
      # created automatically when the authorization flow completes for the first
      # time.
      if os.path.exists("token.json"):
         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
      # If there are no (valid) credentials available, let the user log in.
      if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file(
              "credentials.json", SCOPES
          )
          creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
          token.write(creds.to_json())

      try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
          print("No data found.")
          return

        if values:
           pd.set_option('display.max_columns', None)
           print(pd.DataFrame(values))
           with open('spreadsheet.csv', 'w', newline='') as file:
              writer = csv.writer(file)
              writer.writerows(values)

        #for row in values:
        #  print(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]},{row[8]},{row[9]},{row[10]}")
      except HttpError as err:
        print(err)

#####Sleeper Player Data#####
sleeper_data(funtiontype='runplayerdata')
#####Sleeper User Info#####       
sleeper_data(funtiontype='user',userid=userid)
######Sleeper Single League Info#####
sleeper_data(funtiontype='league',leagueid=leagueid)
#####Sleeper Single League Roster Info#####
sleeper_data(funtiontype='roster',leagueid=leagueid)
#####Sleeper Single League Users Info#####
sleeper_data(funtiontype='allusers',leagueid=leagueid)
#####Sleeper Single League Transactions Info#####
#sleeper_data(funtiontype='transactions',leagueid=leagueid)
#####Sleeper Single League Matchups Info#####
#sleeper_data(funtiontype='matchups',leagueid=leagueid)
#####Sleeper Single League Traded Pick Info#####
#sleeper_data(funtiontype='traded_picks',leagueid=leagueid)
#####Sleeper Single League Traded Pick Info#####
sleeper_data(funtiontype='spread_sheet')
#####Sleeper Single League Draft#####
sleeper_data(funtiontype='draft',draftid=draftid)

