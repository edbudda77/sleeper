import pandas as pd
import csv
import numpy as np

def sleeper_build(funtiontype,userid=None,leagueid=None,week=None,last_year_of_contracts=None):

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
      end_col_name = f'1 or 2 years?'
      new_df = df.loc[:, start_col_name:end_col_name]
      new_df = new_df.rename(columns={'Year of Contract': 'Year_of_Contract', 'Player': 'full_name', 'Per Year $ (In M)': 'Per_Year_M', 'Length Remaining': 'Length_Remaining'})
      new_df[['Owner', 'player_type']] = new_df['Owner'].str.split('-', expand=True)
      new_df['player_type'] = new_df['player_type'].fillna('  ')
      new_df['full_name'] = new_df['full_name'].str.replace(r"\[|'|\]", '', regex=True).str.strip()
      #Update contract values.
      selected_columns = [new_df.columns[7], new_df.columns[8], new_df.columns[9], new_df.columns[10]]
      i = 0
      for column_name in selected_columns:
          i = i + 1
          print(i)
          if i < 4:
             new_df[f'{column_name}'] = np.where(new_df['player_type'] == 'Cut', new_df[f'{column_name}.1'], new_df[f'{column_name}'])
             new_df[f'{column_name}'] = new_df[f'{column_name}'].fillna('  ')
          elif i == 4:
             new_df[f'{column_name}'] = np.where(new_df['player_type'] == 'Cut', 0, new_df[f'{column_name}'])
             new_df[f'{column_name}'] = new_df[f'{column_name}'].fillna('  ')
      
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