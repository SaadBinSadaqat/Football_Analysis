import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import streamlit as st

df=pd.read_csv("football dataset.csv")
st.title("Working with Streamlit and Football Data")
st.header("Football Data Set")

#wrangling / cleaning being done

duplicates = df.duplicated() #none found, so changed all code to comment
num_duplicates = duplicates.sum()
duplicate_rows = df[duplicates]


df_cleaned = df.dropna(subset=['Nationality', 'Position', 'Age'])
df_cleaned['Jersey Number'].fillna(np.random.randint(11, 100), inplace=True)
null_counts = df_cleaned.isnull().sum()
df = df_cleaned

#now performing EDA

# Question 1: Top 5 clubs by the number of goals scored
top_5_clubs_goals = df_cleaned.groupby("Club")["Goals"].sum().sort_values(ascending=False).head(5)


# Bar chart for top 5 clubs by goals scored
fig, ax = plt.subplots()
sns.barplot(x=top_5_clubs_goals.index, y=top_5_clubs_goals.values, palette='magma', ax=ax)

# Annotate each bar with its value
for index, value in enumerate(top_5_clubs_goals.values):
    ax.text(index, value, str(value), ha='center', va='bottom')

ax.set_title('Top 5 Clubs by Goals Scored')
ax.set_xlabel('Club')
ax.set_ylabel('Total Goals')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Set the width of the plot
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(fig)

# Question 2: Club with the highest average goals per match
st.header("Club with Highest Average Goals per Match")
avg_goals_per_match = df_cleaned.groupby("Club")["Goals per match"].mean().idxmax()
st.write(avg_goals_per_match)

# Question 3: Top 3 goal scorers
st.header("Top 3 Goal Scorers")
top_3_goal_scorers = df_cleaned.nlargest(3, "Goals")[["Name", "Club", "Goals"]]
st.write(top_3_goal_scorers)

# Calculate total goals scored with right foot and left foot
left_foot_goals = int(df_cleaned['Goals with left foot'].sum())
right_foot_goals = int(df_cleaned['Goals with right foot'].sum())

# Create a Streamlit app
st.subheader('Goals Distribution by Dominant Foot')

# Bar chart for goals distribution by dominant foot
fig, ax = plt.subplots(figsize=(4, 4))
sns.barplot(x=['Left Foot', 'Right Foot'], y=[left_foot_goals, right_foot_goals], palette='magma', ax=ax)

# Annotate each bar with its value
for index, value in enumerate([left_foot_goals, right_foot_goals]):
    ax.text(index, value, str(value), ha='center', va='bottom')

ax.set_title('Goals Distribution by Dominant Foot')
ax.set_xlabel('Dominant Foot')
ax.set_ylabel('Total Goals')

# Display the plot in Streamlit
st.set_option('deprecation.showPyplotGlobalUse', True)
st.pyplot(fig)

# Question 5: Number of players who scored goals with both left and right feet
players_both_feet_club = df_cleaned[df_cleaned["Goals with left foot"].notna() & df_cleaned["Goals with right foot"].notna()]
club_counts = players_both_feet_club.groupby("Club").size().reset_index(name="Count")

# Select the top 5 clubs with the most players scoring with both feet
top_5_clubs = club_counts.nlargest(5, "Count")

# Plotting the bar chart
st.header("Top 5 Clubs with Most Players Scoring with Both Feet")
fig, ax = plt.subplots()
ax.bar(top_5_clubs["Club"], top_5_clubs["Count"])

plt.xticks(rotation=45)

# Display the plot using Streamlit
st.pyplot(fig)

# # Question 6: Total number of goals scored via penalties
penalties_scored_by_club = df_cleaned.groupby("Club")["Penalties scored"].sum().reset_index()

# Sorting the clubs by penalties scored in descending order
penalties_scored_by_club_sorted = penalties_scored_by_club.sort_values(by="Penalties scored", ascending=False)

# Plotting the bar chart
st.header("Teams with Most Penalties Scored")
fig, ax = plt.subplots()
bars = ax.bar(penalties_scored_by_club_sorted["Club"], penalties_scored_by_club_sorted["Penalties scored"], color='skyblue')

# Adding labels to the bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval), va='bottom')

# Rotating x-axis labels by 45 degrees
plt.xticks(rotation=45, ha='right')

# Displaying the plot using Streamlit
st.pyplot(fig)


##Penalties scorer top 5

top_penalty_scorers = df_cleaned.sort_values(by="Penalties scored", ascending=False).head(5)
top_penalty_scorers.set_index("Name", inplace=True)

# Display the top 5 penalty scorers in a bar chart
st.header("Top 5 Penalty Scorers")
st.bar_chart(top_penalty_scorers["Penalties scored"])

# Display the values on top of the bars
for player, penalty in top_penalty_scorers.iterrows():
    st.text(f"{player}: {penalty['Penalties scored']}")

##PENALTIES SAVERS
    
top_penalty_savers = df_cleaned[df_cleaned['Position'] == 'Goalkeeper'].sort_values(by="Penalties saved", ascending=False).head(5)

# Set goalkeeper names as the index
top_penalty_savers.set_index("Name", inplace=True)

# Display the top 5 penalty-saving goalkeepers in a bar chart
st.header("Top 5 Penalty-Saving Goalkeepers")
st.bar_chart(top_penalty_savers["Penalties saved"])

# Display the values on top of the bars
for goalkeeper, penalties_saved in top_penalty_savers.iterrows():
    st.text(f"{goalkeeper}: {penalties_saved['Penalties saved']}")

##CREATING A NEW COLUMN IN DF
    
df_cleaned['Offsides Goal Ratio'] = df_cleaned['Offsides'] / df_cleaned['Goals']

# Display the updated DataFrame
st.write(df_cleaned)

##BEST PLAYERS WITH LEAST OFFSIDE RATIO

df_cleaned['Offsides Goal Ratio'] = df_cleaned['Offsides'] / df_cleaned['Goals']

# Filter players with at least 30 goals
df_filtered = df_cleaned[df_cleaned['Goals'] >= 30]

# Select the top 10 players with the least Offsides Goal Ratio
top_10_least_offsides_ratio = df_filtered.nsmallest(10, 'Offsides Goal Ratio')[['Name', 'Offsides Goal Ratio']]

# Plotting the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='Name', y='Offsides Goal Ratio', data=top_10_least_offsides_ratio, palette='viridis')
plt.title('Top 10 Players with Least Offsides Goal Ratio (Minimum 30 Goals)')
plt.xlabel('Player Name')
plt.ylabel('Offsides Goal Ratio')
plt.xticks(rotation=45)
for index, value in enumerate(top_10_least_offsides_ratio['Offsides Goal Ratio']):
    plt.text(index, value, str(round(value, 2)), ha='center', va='bottom')
st.pyplot()

# # Question 8: Top Freekick players
top_3_freekick_specialists = df_filtered.nlargest(3, 'Freekicks scored')

# Plotting the bar chart
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Name', y='Freekicks scored', data=top_3_freekick_specialists, palette='muted', ax=ax)

# Add values on top of the bars
for index, value in enumerate(top_3_freekick_specialists['Freekicks scored']):
    ax.text(index, value, str(value), ha='center', va='bottom')

ax.set_title('Top 3 Free-kick Specialists')
ax.set_xlabel('Player Name')
ax.set_ylabel('Number of Free-kick Goals')
ax.set_xticklabels(top_3_freekick_specialists['Name'], rotation=45)  # Rotate x-axis labels by 45 degrees
plt.tight_layout()

# Display the plot using Streamlit
st.pyplot(fig)


###SIDEBAR
st.sidebar.image('football pic.png')# Add some content to the sidebar
st.sidebar.markdown("<div align='center'><h1>WHO'S THE BEST</h1></div>", unsafe_allow_html=True)


# # Question 9: Number of big chances created by players
# st.header("Number of Big Chances Created")
# total_big_chances_created = df["Big chances created"].sum()
# st.write(total_big_chances_created)

# # Question 10: Most creative player in terms of big chances created
# st.header("Most Creative Player in Terms of Big Chances Created")
# most_creative_player = df.loc[df["Big chances created"].idxmax(), ["Name", "Club", "Big chances created"]]
# st.write(most_creative_player)

# # Question 11: Ratio of goals to shots taken
# st.header("Ratio of Goals to Shots Taken")
# df["Goals to Shots Ratio"] = df["Goals"] / df["Shots"]
# st.write(df["Goals to Shots Ratio"].mean())

# # Question 12: Number of clean sheets recorded by goalkeepers
# st.header("Number of Clean Sheets by Goalkeepers")
# clean_sheets_goalkeepers = df[df["Position"] == "Goalkeeper"]["Clean sheets"].sum()
# st.write(clean_sheets_goalkeepers)

# # Question 13: Tackle success percentage across all players
# st.header("Tackle Success Percentage")
# tackle_success_percentage = df["Tackle success %"].str.rstrip("%").astype(float).mean()
# st.write(tackle_success_percentage)

# # Question 14: Number of interceptions made by players
# st.header("Number of Interceptions Made")
# total_interceptions = df["Interceptions"].sum()
# st.write(total_interceptions)

# # Question 15: Distribution of aerial battles won vs. aerial battles lost
# st.header("Distribution of Aerial Battles Won vs. Lost")
# aerial_battles = df[["Aerial battles won", "Aerial battles lost"]].sum()
# st.bar_chart(aerial_battles)

# # Question 16: Number of own goals scored
# st.header("Number of Own Goals Scored")
# total_own_goals = df["Own goals"].sum()
# st.write(total_own_goals)

# # Question 17: Number of errors leading to goals committed
# st.header("Number of Errors Leading to Goals")
# total_errors_leading_to_goals = df["Errors leading to goal"].sum()
# st.write(total_errors_leading_to_goals)

# # Question 18: Total number of assists provided by players
# st.header("Total Number of Assists Provided")
# total_assists = df["Assists"].sum()
# st.write(total_assists)

# # Question 19: Most prolific assist provider
# st.header("Most Prolific Assist Provider")
# most_prolific_assist_provider = df.loc[df["Assists"].idxmax(), ["Name", "Club", "Assists"]]
# st.write(most_prolific_assist_provider)

# # Question 20: Average number of passes per match
# st.header("Average Number of Passes per Match")
# avg_passes_per_match = df["Passes per match"].mean()
# st.write(avg_passes_per_match)