import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import json
import csv
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def sleeper_data(funtiontype,userid=None,leagueid=None,week=None,draftid=None,SCOPES=None,SAMPLE_SPREADSHEET_ID=None,SAMPLE_RANGE_NAME=None):

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