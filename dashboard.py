#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import os
import os.path

userid = 'beebudda'
week = 0
year = '2024'
last_year_of_contracts = 2028
leaguename = 'mmmc'

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

#######################
# Page configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.theme.enable("dark")

#######################
# Load data
df_reshaped = pd.read_csv('full_roster.csv')

#######################
# Sidebar
with st.sidebar:
    st.title('Manager List')
    
    manager_list = list(df_reshaped.display_name.unique())[::-1]
    
    selected_manager = st.selectbox('Select a Manager', manager_list)
    df_selected_manager = df_reshaped[df_reshaped.display_name == selected_manager]
    df_selected_manager_sorted = df_selected_manager.sort_values(by="display_name", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

#######################
# Dashboard Main Panel
col = st.columns((10))

with col[0]:
    st.markdown('#### Players')

    st.dataframe(df_selected_manager_sorted,
                 column_order=("display_name"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "fantasy_positions": st.column_config.TextColumn(
                        "Pos",
                    ),
                    "Length_Remaining": st.column_config.TextColumn(
                        "Years Remaining",
                     )}
                 )
