import pandas as pd
import numpy as np
import json
import csv
import os
import csv
import os.path
from sleeper_data import sleeper_data
from copy_file import copy_file
from get_value_from_csv import get_value_from_csv

import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1cVkswp7NckK7kxG0sb1m7qH8siA0dtgFZ6p8zorXimg"
SAMPLE_RANGE_NAME = "Player Contracts!A5:P"

userid = 'beebudda'
year = '2025'
startyear = 2025
leaguename = 'mmmc'

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

#####Sleeper Player Data#####
#sleeper_data(funtiontype='runplayerdata')
#####Sleeper User Info#####       
#sleeper_data(funtiontype='user',userid=userid)
######Sleeper Single League Info#####
#sleeper_data(funtiontype='league',leagueid=leagueid)
#####Sleeper Single League Roster Info#####
#sleeper_data(funtiontype='roster',leagueid=leagueid)
#####Sleeper Single League Users Info#####
#sleeper_data(funtiontype='allusers',leagueid=leagueid)
#####Sleeper Single League Transactions Info#####
##sleeper_data(funtiontype='transactions',leagueid=leagueid)
#####Sleeper Single League Matchups Info#####
##sleeper_data(funtiontype='matchups',leagueid=leagueid)
#####Sleeper Single League Traded Pick Info#####
##sleeper_data(funtiontype='traded_picks',leagueid=leagueid)
#####Sleeper Single League Traded Pick Info#####
#sleeper_data(funtiontype='spread_sheet',SCOPES=SCOPES,SAMPLE_SPREADSHEET_ID=SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME=SAMPLE_RANGE_NAME)
#####Sleeper Single League Draft#####
#sleeper_data(funtiontype='draft',draftid=draftid)

def user_league(leagueid,leaguename,startyear):

   #Sleeper Single League Users Info
   file_path = f"C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\{leaguename}\\Extract\\users\\leaguelist.csv"
   filename = f"user_leages.json"
   leagueusers = requests.get(f'https://api.sleeper.app/v1/league/{leagueid}/users')
   leagueusersjson = leagueusers.json()
   with open(filename, "w") as f:
      json.dump(leagueusersjson, f, indent=1)
   leagueusersjson = pd.json_normalize(leagueusersjson, max_level=1)
   leagueusersjson.columns = leagueusersjson.columns.str.replace('.', '_')
   columns_to_keep = ['display_name', 'user_id', 'league_id']
   usersandleagues = leagueusersjson[columns_to_keep].drop_duplicates()
   usersandleagues.to_csv(f"C:\\Users\\Ezekiel Budda\\Desktop\\Python\\sleeper\\{leaguename}\\Extract\\users\\usersandleagues.csv", index=False)
   display_name = usersandleagues.iloc[0]['display_name']
   user_id = usersandleagues.iloc[0]['user_id']
   current_year = {startyear}
   for i in range(startyear, 0, -1):
      try:
         userleagues = requests.get(f'https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{i}', timeout=5)
         if userleagues.status_code == 404:
            break
         else:
            userleaguesjson = userleagues.json()
            with open(filename, "w") as f:
               json.dump(userleaguesjson, f, indent=1)
            userleaguesjson = pd.json_normalize(userleaguesjson, max_level=1)
            userleaguesjson.columns = userleaguesjson.columns.str.replace('.', '_')
            columns_to_keep = ['league_id', 'name', 'season']
            userleaguesjson = userleaguesjson[columns_to_keep].drop_duplicates()
            file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0
            userleaguesjson.to_csv(file_path, mode='a', header=not file_exists, index=False)
      except requests.exceptions.RequestException as e:
         print(f"No more leagues found for {display_name}")
    
   #if not os.path.exists(default_folder):
   #   os.makedirs(default_folder)
      
user_league(leagueid=leagueid,leaguename=leaguename,startyear=startyear)


