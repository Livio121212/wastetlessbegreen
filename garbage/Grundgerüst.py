import streamlit as st
              
# open first the setting page to define flate-name and inhabitants
if "pages" not in st.session_state:
    st.session_state ["page"] = "settings"

# Function to change between the pages
def change_page(new_page):
    st.session_state["page"] = new_page


if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""
if "roommates" not in st.session_state:
    st.session_state["roommates"] = []
if "room_mate_input" not in st.session_state:
    st.session_state["room_mate_input"] = ""
if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = False

# sidebar; titel
st.sidebar.title("Navigation")

# sidebar: change de side by unsing the buttons
page_selection = st.sidebar.selectbox("Overview:", ["overview", "Livio", "Flurin"])
if page_selection != st.session_state["page"]:
    st.session_state["page"] = page_selection
if st.sidebar.button("Fridge"):
    change_page("fridge")
if st.sidebar.button("Recipes"):
    change_page("recipes")
if st.sidebar.button("Settings"):
    change_page("settings")

# Anzeigelogik für jede Seite
if st.session_state["page"] == "overview":
    st.title("overview")
    st.write('Willkommen auf der Startseite deiner App.')
    st.write('Hier kannst du allgemeine Informationen anzeigen.')
elif st.session_state["page"] == "fridge":
    st.title("fridge")
    st.write('Dies ist der Inhalt von Seite 1.')
    st.text_input('Gib deinen Namen ein:', key='name_input_page1')
    st.button('Bestätigen')
elif st.session_state["page"] == "recipes":
    st.title("recipes")
    st.write('Dies ist der Inhalt von Seite 2.')
    st.slider('Wähle einen Wert:', 0, 100, 50, key='slider_page2')
elif st.session_state["page"] == "settings":
    if not st.session_state["setup_finished"]:
        if st.session_state["flate_name"] == "":
            setup_flat_name()
        else:
            setup_roommates()
    else:
        settings_page()




elif st.session_state["page"] == "Livio":
    st.title("Livio")
    st.write('Dies ist der Inhalt von Seite 1.')
    st.text_input('Gib deinen Namen ein:', key='name_input_page1')
    st.button('Bestätigen')