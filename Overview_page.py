import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]
if "expenses_over_time" not in st.session_state:
    st.session_state["expenses_over_time"] = pd.DataFrame([
        {"Date": "2024-11-01", "Roommate": "Livio", "Expense": 20},
        {"Date": "2024-11-02", "Roommate": "Flurin", "Expense": 15},
        {"Date": "2024-11-03", "Roommate": "Anderin", "Expense": 10},
        {"Date": "2024-11-05", "Roommate": "Livio", "Expense": 5},
        {"Date": "2024-11-06", "Roommate": "Flurin", "Expense": 20},
        {"Date": "2024-11-07", "Roommate": "Anderin", "Expense": 15},
    ]) # Here we must integrate the timestamp of the purchase or scan

if "cooking_history" not in st.session_state:
    # Sample data structure for cumulative recipe ratings
    st.session_state["cooking_history"] = pd.DataFrame([
        {"Date": "2024-11-01", "Person": "Livio", "Recipe": "Pasta Carbonara"},
        {"Date": "2024-11-02", "Person": "Flurin", "Recipe": "Chicken Curry"},
        {"Date": "2024-11-03", "Person": "Anderin", "Recipe": "Vegetable Stir Fry"},
        {"Date": "2024-11-04", "Person": "Livio", "Recipe": "Salad"},
        {"Date": "2024-11-06", "Person": "Flurin", "Recipe": "Beef Stew"},
        {"Date": "2024-11-08", "Person": "Anderin", "Recipe": "Pancakes"},
        # Here we must integrate the timestamp of the rating
    ])

def overview_page(): 
    # Sets the title to "Overview: Name of the flat"
    title = f"Overview: {st.session_state['flate_name']}" if st.session_state["flate_name"] else "Overview"
    st.title(title)
    st.write("Welcome to the main page of your app.")
    st.write("Here you can display general information.")


# from here infos for line chart finance




# Convert 'Date' column to datetime format for plotting
st.session_state["expenses_over_time"]["Date"] = pd.to_datetime(st.session_state["expenses_over_time"]["Date"])

# Calculate cumulative expenses per roommate and for the flat (total)
expenses_df = st.session_state["expenses_over_time"].copy()
expenses_df["Cumulative Expense"] = expenses_df.groupby("Roommate")["Expense"].cumsum()

# Calculate total expenses for the entire flat on each date
total_expenses_df = expenses_df.groupby("Date")["Expense"].sum().cumsum().reset_index()
total_expenses_df["Roommate"] = "Total Flat"  # Label for the entire flat's cumulative expenses

# Append the total expenses line to the individual roommate expenses for plotting
expenses_df = pd.concat([expenses_df, total_expenses_df.rename(columns={"Expense": "Cumulative Expense"})])

# Plotting
fig = px.line(
    expenses_df, 
    x="Date", 
    y="Cumulative Expense", 
    color="Roommate", 
    title="Cumulative Expenses Over Time",
    labels={"Cumulative Expense": "Total Expenses (CHF)", "Date": "Date", "Roommate": "Legend"}
)



# From here infos for line chart how much each roomate cooked




# Convert 'Date' column to datetime format
st.session_state["cooking_history"]["Date"] = pd.to_datetime(st.session_state["cooking_history"]["Date"])

# Calculate cumulative count of recipes rated per roommate
ratings_df = st.session_state["cooking_history"].copy()
ratings_df["Recipes Rated"] = ratings_df.groupby("Person").cumcount() + 1


# Aggregate data to get cumulative recipes rated over time for each roommate
# If roommates are not rating recipes every day, we want to fill in missing days
all_dates = pd.date_range(ratings_df["Date"].min(), ratings_df["Date"].max(), freq="D")
cumulative_ratings = []

for roommate in st.session_state["roommates"]:
    roommate_data = ratings_df[ratings_df["Person"] == roommate][["Date", "Recipes Rated"]]
    roommate_data = roommate_data.set_index("Date").reindex(all_dates).fillna(method="ffill").fillna(0)
    roommate_data = roommate_data.reset_index().rename(columns={"index": "Date"})
    roommate_data["Person"] = roommate
    cumulative_ratings.append(roommate_data)

# Combine cumulative ratings data for plotting
cumulative_ratings_df = pd.concat(cumulative_ratings)

# Plotting the cumulative number of recipes rated per roommate
fig = px.line(
    cumulative_ratings_df,
    x="Date",
    y="Recipes Rated",
    color="Person",
    title="Cumulative Recipes Rated Over Time",
    labels={"Recipes Rated": "Total Recipes Rated", "Date": "Date", "Person": "Roommate"}
)



# Display the line chart in Streamlit
st.plotly_chart(fig)