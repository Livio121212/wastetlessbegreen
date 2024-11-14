import streamlit as st
import json
import os
from datetime import datetime
from settings_page import setup_flat_name, setup_roommates, settingspage
from fridge_page import fridge_page
from barcode_page import barcode_page
from recipe_page import recipepage

# Ensure all session state variables are initialized
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""
if "roommates" not in st.session_state:
    st.session_state["roommates"] = []
if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "settings"
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {}
if "expenses" not in st.session_state:
    st.session_state["expenses"] = {}
if "purchases" not in st.session_state:
    st.session_state["purchases"] = {}
if "consumed" not in st.session_state:
    st.session_state["consumed"] = {}
if "recipe_suggestions" not in st.session_state:
    st.session_state["recipe_suggestions"] = []
if "selected_recipe" not in st.session_state:
    st.session_state["selected_recipe"] = None
if "selected_recipe_link" not in st.session_state:
    st.session_state["selected_recipe_link"] = None
if "cooking_history" not in st.session_state:
    st.session_state["cooking_history"] = []
if "recipe_links" not in st.session_state:
    st.session_state["recipe_links"] = {}
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "data" not in st.session_state:
    st.session_state["data"] = {}

# Function to register a user
def register_user(username, password):
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            users = json.load(file)
    else:
        users = {}

    if username in users:
        st.error("Username already exists!")
        return False
    else:
        users[username] = password
        with open("users.json", "w") as file:
            json.dump(users, file)
        return True

# Function to log in a user
def login_user(username, password):
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            users = json.load(file)
    else:
        st.error("No users found! Please register first.")
        return False

    if username in users and users[username] == password:
        return True
    else:
        st.error("Incorrect username or password!")
        return False

# Function to save WG data
def save_data(username, data):
    data_file = f"{username}_data.json"
    with open(data_file, "w") as file:
        json.dump(data, file)

# Function to load WG data
def load_data(username):
    data_file = f"{username}_data.json"
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    else:
        return {}

# Show menu only if the user is not logged in
def authentication():
    if not st.session_state["logged_in"]:
        menu = st.sidebar.selectbox("Menu", ["Log In", "Register"])

        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if menu == "Register":
            if st.sidebar.button("Register"):
                if register_user(username, password):
                    st.success("Successfully registered! Please log in.")
        elif menu == "Log In":
            if st.sidebar.button("Log In"):
                if login_user(username, password):
                    st.success(f"Welcome, {username}!")
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    # Load WG data
                    st.session_state["data"] = load_data(username)
                    # Load WG data into the session state
                    st.session_state.update(st.session_state["data"])

# Function to automatically save WG data
def auto_save():
    # Nur speichern, wenn "username" im session_state gesetzt ist
    if "username" in st.session_state and st.session_state["username"]:
        st.session_state["data"] = {
            "flate_name": st.session_state.get("flate_name", ""),
            "roommates": st.session_state.get("roommates", []),
            "setup_finished": st.session_state.get("setup_finished", False),
            "inventory": st.session_state.get("inventory", {}),
            "expenses": st.session_state.get("expenses", {}),
            "purchases": st.session_state.get("purchases", {}),
            "consumed": st.session_state.get("consumed", {}),
            "recipe_suggestions": st.session_state.get("recipe_suggestions", []),
            "selected_recipe": st.session_state.get("selected_recipe", None),
            "selected_recipe_link": st.session_state.get("selected_recipe_link", None),
            "cooking_history": st.session_state.get("cooking_history", []),
            "recipe_links": st.session_state.get("recipe_links", {})
        }
        save_data(st.session_state["username"], st.session_state["data"])



# Funktion zum Löschen des Accounts
def delete_account():
    with st.expander("Delete Account"):
        st.warning("This action is irreversible. Deleting your account will remove all your data.")
        confirm = st.button("Delete Account")
        if confirm:
            delete_data()
            st.session_state["logged_in"] = False


def delete_data():
    username = st.session_state.get("username")
    if username:
        # Entferne den Benutzer aus der Datei users.json
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                users = json.load(file)
            if username in users:
                del users[username]
                with open("users.json", "w") as file:
                    json.dump(users, file)
        
        # Lösche die spezifische Daten-Datei des Benutzers
        data_file = f"{username}_data.json"
        if os.path.exists(data_file):
            os.remove(data_file)
    st.session_state.clear()
        


# If the user is logged in, show the main page
if st.session_state["logged_in"]:
    # Sidebar navigation with buttons (no menu selection here)
    st.sidebar.title("Navigation")
    if st.sidebar.button("Overview"):
        st.session_state["page"] = "overview"
    if st.sidebar.button("Fridge"):
        st.session_state["page"] = "fridge"
    if st.sidebar.button("Scan"):
        st.session_state["page"] = "scan"
    if st.sidebar.button("Recipes"):
        st.session_state["page"] = "recipes"
    if st.sidebar.button("Settings"):
        st.session_state["page"] = "settings"

    # Make the "Log Out" button red
    if st.sidebar.button("Log Out", type="primary"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["data"] = {}
        st.experimental_set_query_params()  # Simulate a rerun by setting query params
        st.stop()  # End execution to reload the app

    # Page display logic for the selected page
    if st.session_state["page"] == "overview":
        st.title(f"Overview: {st.session_state['flate_name']}")
        st.write("Welcome to your WG overview page!")
        auto_save()  # Automatically save data
    elif st.session_state["page"] == "fridge":
        fridge_page()
        auto_save()  # Automatically save data
    elif st.session_state["page"] == "scan":
        barcode_page()
        auto_save()  # Automatically save data
    elif st.session_state["page"] == "recipes":
        recipepage()
        auto_save()  # Automatically save data
    elif st.session_state["page"] == "settings":
        if not st.session_state["setup_finished"]:
            if st.session_state["flate_name"] == "":
                setup_flat_name()
            else:
                setup_roommates()
        else:
            settingspage()
            delete_account()
        auto_save()  # Automatically save data
else:
    st.title("Wasteless")
    st.write("Please log in or register to continue.")
    authentication()
