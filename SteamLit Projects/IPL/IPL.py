import pandas as pd
import plotly.express as px
import streamlit as st
import os
import warnings

st.set_page_config(page_title="Kesa laga", page_icon=":smile:", layout="wide")
st.title(':smile: Testing')

col1, col2 = st.columns((2))
# Load datasets
deliver = pd.read_csv("datasets/deliveries.csv")
matches = pd.read_csv("datasets/matches.csv")

# Merge datasets
df = deliver.merge(matches, left_on='match_id', right_on='id',how='inner')

# Data cleaning
matches = matches.dropna(subset=['winner'])
matches['player_of_match'] = matches['player_of_match'].fillna('Unknown')
matches.drop(['id', 'city', 'method'], axis=1, inplace=True)
# Mapping dictionary for old names to standardized names
team_name_mapping = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings',
    'Rising Pune Supergiants': 'Pune Warriors',
    'Rising Pune Supergiant': 'Pune Warriors',
    'Gujarat Lions': 'Gujarat Titans',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Royal Challengers Bengaluru': 'Royal Challengers Bangalore',
}

team_columns = ['winner', 'team1', 'team2', 'toss_winner']

# Replace the team names in the 'winner' column
df[team_columns] = df[team_columns].replace(team_name_mapping)

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sidebar filters for year
st.sidebar.header("Choose your filters:")
available_years = df['date'].dt.year.unique()


Years = st.sidebar.multiselect(
    "Year: ",
    options=sorted(available_years),  # Sort years for better UX
    default=available_years.max()
)

# Sidebar filters for venue

venue_list = df['venue'].unique()
venue = st.sidebar.multiselect(
    "Pick your venue: ",
    options=sorted(venue_list)  # Sort venues for better UX
)

# Filter data based on selected years and venues
if Years:
    df = df[df['date'].dt.year.isin(Years)]
if venue:
    df = df[df['venue'].isin(venue)]

# Calculate top 10 batsmen based on the filtered data
batsman = df[['batter', 'batsman_runs']].groupby('batter').sum().sort_values('batsman_runs', ascending=False).head(10).reset_index()
bowler = df[['bowler', 'total_runs']].groupby('bowler').sum().sort_values('total_runs', ascending=False).head(10).reset_index()

# Display the results
with col1:
    st.write("Top 10 Batsmen based on selected filters:")
    st.dataframe(batsman)
    fig1=px.pie(batsman,names='batter',values='batsman_runs', hover_name='batter')
    st.plotly_chart(fig1)
with col2:
    st.write("Top 10 Batsmen based on selected filters:")
    st.dataframe(bowler)
    fig1=px.pie(bowler,names='bowler',values='total_runs')
    st.plotly_chart(fig1)

st.dataframe(df['winner'].unique())
