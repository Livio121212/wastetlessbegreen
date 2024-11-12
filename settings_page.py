import streamlit as st

# Setup-Seite für die Eingabe des WG-Namens
def setup_flat_name():
    st.title("🏠 Wasteless App - Setup")
    flate_name = st.text_input("Please enter your flat name")
    if st.button("Confirm Flat Name"): 
        if flate_name:
            st.session_state["flate_name"] = flate_name
            st.success(f"You successfully saved your flate name:{flate_name}")
        else:
            st.warning("Please enter a flat_name")

# Hauptseite zur Eingabe der Mitbewohner
def setup_roommates():
    st.title(f"Welcome to {st.session_state['flate_name']}!")
    room_mate = st.text_input("Please enter the name of a roommate", key="room_mate_input")
    if st.button("Add a new roommate"):
        add_roommate(room_mate)
    display_roommates()
    if st.button("Finish"):
        st.session_state["setup_finished"] = True

# Funktion zum Hinzufügen eines Mitbewohners
def add_roommate(room_mate):
    if room_mate and room_mate not in st.session_state["roommates"]:
        st.session_state["roommates"].append(room_mate)
        st.success(f"Roommate {room_mate} has been added!")
    elif room_mate in st.session_state["roommates"]:
        st.warning(f"Roommate {room_mate} is already in the list!")

# Funktion zur Anzeige der Mitbewohner
def display_roommates():
    if st.session_state["roommates"]:
        st.write("Current roommates:")
        for mate in st.session_state["roommates"]:
            st.write(f"- {mate}")

# Seite für Einstellungen, wenn das Setup abgeschlossen ist
def settingspage():
    st.write("Congratulations, your settings are done.")
    change_flat_name()
    manage_roommates()

# Funktion zum Ändern des WG-Namens
def change_flat_name():
    with st.expander("Flat name"):
        flate_name = st.text_input("Please enter your flat name")
        if st.button("Change Flat Name"):
            if flate_name:
                st.session_state["flate_name"] = flate_name
                st.success(f"You successfully changed your flat name to {flate_name}!")
            else:
                st.warning("Please enter a new flat name")

# Funktion zur Verwaltung der Mitbewohner
def manage_roommates():
    with st.expander("Roommates"):
        room_mate = st.text_input("Please enter the name of a roommate", key="new_room_mate_input")
        if st.button("Add new roommate"):
            add_roommate(room_mate)
        display_roommates()
        remove_roommate()

# Funktion zum Entfernen eines Mitbewohners
def remove_roommate():
    if st.session_state["roommates"]:
        roommate_to_remove = st.selectbox("Select a roommate to remove", st.session_state["roommates"])
        if st.button("Remove roommate"):
            if roommate_to_remove in st.session_state["roommates"]:
                st.session_state["roommates"].remove(roommate_to_remove)
                st.success(f"Roommate {roommate_to_remove} has been removed!")


# Ablauf
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""
if "roommates" not in st.session_state:
    st.session_state["roommates"] = []
if "room_mate_input" not in st.session_state:
    st.session_state["room_mate_input"] = ""
if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = False
    
if not st.session_state["setup_finished"]:
    if st.session_state["flate_name"] == "":
        setup_flat_name()
    else:
        setup_roommates()
else:
    settingspage()
