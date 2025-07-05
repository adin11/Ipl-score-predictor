import streamlit as st
import pandas as pd
import numpy as np 
import joblib

# Page Configurations:
st.set_page_config(
    page_title="FinalScore Insight",
    page_icon="🏏",
)

# Load the model and scaler
model = joblib.load("artifacts/model.joblib")

st.title("🏏 FinalScore Insight")
st.markdown("<h2 style='text-align: left; font-size: 20px; font-weight: bold;'> Enter live match details and forecast the target score with precision — minimum 5 overs required. </h2>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Dropdowns for teams
bat_teams = [
    "Chennai Super Kings", "Delhi Capitals", "Punjab Kings",
    "Kolkata Knight Riders", "Mumbai Indians", "Rajasthan Royals",
    "Royal Challengers Bangalore", "Sunrisers Hyderabad"
]
bowl_teams = bat_teams.copy()

# Dropdown for selecting teams
bat_team = st.selectbox("Select Batting Team", bat_teams)
bowl_team = st.selectbox("Select Bowling Team", bowl_teams)

# Validate that the teams are different
if bat_team == bowl_team:
    st.error("Batting team and Bowling team cannot be the same. Please select different teams.")

# Input fields for match details
runs = st.number_input("Runs Scored", min_value=0, step=1, value=0, help="Enter the current runs")
wickets = st.number_input("Wickets Fallen", min_value=0, step=1, value=0, help="Enter the current number of wickets down")
overs = st.number_input("Overs Played", min_value=0.0, max_value=20.0, step=0.1, value=0.0, help="Enter the current number of overs completed")
runs_last_5 = st.number_input("Runs Scored in Last 5 Overs", min_value=0, step=1, value=0, help="Enter the runs scored in the last 5 overs")
wickets_last_5 = st.number_input("Wickets Fallen in Last 5 Overs", min_value=0, step=1, value=0, help="Enter the wickets fallen in the last 5 overs")

# Validation flags
valid_inputs = True
if runs_last_5 > runs:
    st.error("Runs scored in the last 5 overs cannot be more than the current runs.")
    valid_inputs = False
if wickets_last_5 > wickets:
    st.error("Wickets fallen in the last 5 overs cannot be more than the current wickets.")
    valid_inputs = False
if overs < 5:
    st.error("Overs played must be greater than 5 for prediction.")
    valid_inputs = False
if bat_team == bowl_team:
    valid_inputs = False


# Prepare manual data dictionary
manual_data = {
    'runs': [runs],  # Total runs scored by the batting team
    'wickets': [wickets],  # Number of wickets taken
    'overs': [overs],  # Total overs played
    'runs_last_5': [runs_last_5],  # Runs scored in the last 5 overs
    'wickets_last_5': [wickets_last_5],  # Wickets taken in the last 5 overs
    'bat_team_Delhi Daredevils': [1 if bat_team == "Delhi Daredevils" else 0],  
    'bat_team_Kings XI Punjab': [1 if bat_team == "Kings XI Punjab" else 0],
    'bat_team_Kolkata Knight Riders': [1 if bat_team == "Kolkata Knight Riders" else 0],
    'bat_team_Mumbai Indians': [1 if bat_team == "Mumbai Indians" else 0],
    'bat_team_Rajasthan Royals': [1 if bat_team == "Rajasthan Royals" else 0],
    'bat_team_Royal Challengers Bangalore': [1 if bat_team == "Royal Challengers Bangalore" else 0],
    'bat_team_Sunrisers Hyderabad': [1 if bat_team == "Sunrisers Hyderabad" else 0],
    'bowl_team_Delhi Daredevils': [1 if bowl_team == "Delhi Daredevils" else 0],
    'bowl_team_Kings XI Punjab': [1 if bowl_team == "Kings XI Punjab" else 0],
    'bowl_team_Kolkata Knight Riders': [1 if bowl_team == "Kolkata Knight Riders" else 0],
    'bowl_team_Mumbai Indians': [1 if bowl_team == "Mumbai Indians" else 0],
    'bowl_team_Rajasthan Royals': [1 if bowl_team == "Rajasthan Royals" else 0],
    'bowl_team_Royal Challengers Bangalore': [1 if bowl_team == "Royal Challengers Bangalore" else 0],
    'bowl_team_Sunrisers Hyderabad': [1 if bowl_team == "Sunrisers Hyderabad" else 0]
}

# Convert the manual data to a DataFrame
manual_data_df = pd.DataFrame(manual_data)

# One-hot encoding and aligning columns
manual_data_encoded = pd.get_dummies(manual_data_df)

# Ensure the encoded columns match with the model's training data
manual_data_encoded = manual_data_encoded.reindex(columns=model.feature_names_in_, fill_value=0)


# Prediction logic
if st.button("Estimate Target Score"):
    if valid_inputs:
        predicted_score = model.predict(manual_data_encoded)
        st.success(f"Estimated Target : {predicted_score[0]:.2f}")
    else:
        st.error("Please fix the errors above before making a prediction.")

# Footer Section

st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
    <h4>A Project by ~ Adin Raja ✌️</h4>
    <p>
        <a href='https://github.com/adin11' target='_blank'>GitHub</a> | 
        <a href='https://www.linkedin.com/in/adin-raja-492a78194/' target='_blank'>LinkedIn</a> | 
        <a href='mailto:adinraja78@gmail.com'>Email</a>
    </p>
    <small>© 2024 Adin Raja. All rights reserved.</small>
</div>
""", unsafe_allow_html=True)

# Optional Sidebar for About Section
with st.sidebar: 
    with st.sidebar:
     st.markdown("### About This App") 

    st.info(
        """
        A ML Powered tool to predict the first inning score of an IPL match.  
        Trained the model using ball-by-ball historical data.  

        **Made by ~ Adin Raja**
        """
    )
    st.markdown("### 📬 Contact") 
    st.write("""
    - ✉️ Email: [adinraja78@gmail.com](mailto:your_email@example.com)
    - 💼 [LinkedIn](https://www.linkedin.com/in/adin-raja-492a78194/)
    - 🖥️ [GitHub](https://github.com/adin11)
    """)