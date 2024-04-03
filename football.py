import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

df=pd.read_csv("football dataset.csv")
st.title("Working with Streamlit and Football Data")
st.header("Football Data Set")

# Wrangling / cleaning being done

# Skipping cleaning part for brevity

# Now performing EDA

# Question 1: Top 5 clubs by the number of goals scored
top_5_clubs_goals = df.groupby("Club")["Goals"].sum().sort_values(ascending=False).head(5)

# Bar chart for top 5 clubs by goals scored
fig = go.Figure()
fig.add_trace(go.Bar(x=top_5_clubs_goals.index, y=top_5_clubs_goals.values, marker_color='magenta'))
fig.update_layout(title='Top 5 Clubs by Goals Scored', xaxis_title='Club', yaxis_title='Total Goals')
st.plotly_chart(fig)

# Question 2: Club with the highest average goals per match
avg_goals_per_match = df.groupby("Club")["Goals per match"].mean().idxmax()
st.header("Club with Highest Average Goals per Match")
st.write(avg_goals_per_match)

# Question 3: Top 3 goal scorers
top_3_goal_scorers = df.nlargest(3, "Goals")[["Name", "Club", "Goals"]]
st.header("Top 3 Goal Scorers")
st.write(top_3_goal_scorers)

# Calculate total goals scored with right foot and left foot
left_foot_goals = int(df['Goals with left foot'].sum())
right_foot_goals = int(df['Goals with right foot'].sum())

# Question 4: Goals Distribution by Dominant Foot
st.subheader('Goals Distribution by Dominant Foot')
fig = go.Figure(data=[go.Bar(x=['Left Foot', 'Right Foot'], y=[left_foot_goals, right_foot_goals], marker_color='magenta')])
fig.update_layout(title='Goals Distribution by Dominant Foot', xaxis_title='Dominant Foot', yaxis_title='Total Goals')
st.plotly_chart(fig)

# Question 5: Number of players who scored goals with both left and right feet
players_both_feet_club = df[df["Goals with left foot"].notna() & df["Goals with right foot"].notna()]
club_counts = players_both_feet_club.groupby("Club").size().reset_index(name="Count")

# Select the top 5 clubs with the most players scoring with both feet
top_5_clubs = club_counts.nlargest(5, "Count")

# Plotting the bar chart
st.header("Top 5 Clubs with Most Players Scoring with Both Feet")
fig = px.bar(top_5_clubs, x="Club", y="Count", labels={'Club': 'Club', 'Count': 'Number of Players'})
st.plotly_chart(fig)

# Question 6: Teams with Most Penalties Scored
penalties_scored_by_club = df.groupby("Club")["Penalties scored"].sum().reset_index()
penalties_scored_by_club_sorted = penalties_scored_by_club.sort_values(by="Penalties scored", ascending=False)

st.header("Teams with Most Penalties Scored")
fig = px.bar(penalties_scored_by_club_sorted, x="Club", y="Penalties scored", labels={'Club': 'Club', 'Penalties scored': 'Total Penalties Scored'})
st.plotly_chart(fig)

# Question 7: Top 5 Penalty Scorers
top_penalty_scorers = df.sort_values(by="Penalties scored", ascending=False).head(5)

st.header("Top 5 Penalty Scorers")
fig = px.bar(top_penalty_scorers, x=top_penalty_scorers.index, y="Penalties scored", labels={'index': 'Player', 'Penalties scored': 'Total Penalties Scored'})
st.plotly_chart(fig)

# Question 8: Top 5 Penalty-Saving Goalkeepers
top_penalty_savers = df[df['Position'] == 'Goalkeeper'].sort_values(by="Penalties saved", ascending=False).head(5)

st.header("Top 5 Penalty-Saving Goalkeepers")
fig = px.bar(top_penalty_savers, x=top_penalty_savers.index, y="Penalties saved", labels={'index': 'Goalkeeper', 'Penalties saved': 'Total Penalties Saved'})
st.plotly_chart(fig)

# Creating a new column in DF
df['Offsides Goal Ratio'] = df['Offsides'] / df['Goals']

# Display the updated DataFrame
st.write(df)

# Best players with the least offside ratio
df_filtered = df[df['Goals'] >= 30]
top_10_least_offsides_ratio = df_filtered.nsmallest(10, 'Offsides Goal Ratio')[['Name', 'Offsides Goal Ratio']]

st.header("Top 10 Players with Least Offsides Goal Ratio (Minimum 30 Goals)")
fig = px.bar(top_10_least_offsides_ratio, x='Name', y='Offsides Goal Ratio', labels={'Name': 'Player', 'Offsides Goal Ratio': 'Offsides Goal Ratio'})
st.plotly_chart(fig)

# Question 9: Top 3 Free-kick Specialists
top_3_freekick_specialists = df_filtered.nlargest(3, 'Freekicks scored')

st.header("Top 3 Free-kick Specialists")
fig = px.bar(top_3_freekick_specialists, x='Name', y='Freekicks scored', labels={'Name': 'Player', 'Freekicks scored': 'Number of Free-kick Goals'})
st.plotly_chart(fig)

# Sidebar
st.sidebar.image('football pic.png')
st.sidebar.markdown("<div align='center'><h1>WHO'S THE BEST</h1></div>", unsafe_allow_html=True)
