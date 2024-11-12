import streamlit as st

# Checks whether certain keys are present in st.session_state. If not, they are initialized with default values
if "flate_name" not in st.session_state: 
    st.session_state["flate_name"] = ""

if "roommates" not in st.session_state:
    st.session_state["roommates"] = []

if "room_mate_input" not in st.session_state:
    st.session_state["room_mate_input"] = ""

if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = False

# Setup-Seite for the flate name (just when there is not one)
if not st.session_state["setup_finished"] and st.session_state["flate_name"] == "":
    st.title("🏠 Wasteless App - Setup")
    flate_name = st.text_input("Please enter your flat name")
    if st.button("Confirm Flat Name"):
        if flate_name:  # Überprüfen, ob ein Name eingegeben wurde
            st.session_state["flate_name"] = flate_name  # Speichere den Namen

# set up for the roommates
if not st.session_state["setup_finished"] and st.session_state["flate_name"]: # checks if there already flat_name and if there are entered any roomates
    st.title(f"Welcome to {st.session_state['flate_name']}!")
    room_mate = st.text_input("Please enter the name of a roommate", key="room_mate_input")
    if st.button("Add a new roommate"):
        if room_mate:  # Check if a name has been entered
            if room_mate not in st.session_state["roommates"]:  # Check if the name does not already exist
                st.session_state["roommates"].append(room_mate)  # add the name to room_mate
                st.success(f"Roommate {room_mate} has been added!") 
            else:
                st.warning(f"Roommate {room_mate} is already in the list!")
    # Show the list of roommates
    if st.session_state["roommates"]:
        st.write("Current roommates:")
        for mate in st.session_state["roommates"]:
            st.write(f"- {mate}")
    # “Finish” button to complete the settings
    if st.button("Finish"):
        st.session_state["setup_finished"] = True  #Sets the status that the setup is complete

# Page when de set-up is finished
if st.session_state["setup_finished"]:
    st.write("Congratulations, your settings are done.")
    with st.expander("Flat name"):
        flate_name = st.text_input("Please enter your flat name")
        if st.button("Change Flat Name"):
            if flate_name:  # Überprüfen, ob ein Name eingegeben wurde
                st.session_state["flate_name"] = flate_name  # Speichere den Namen
                st.success(f"You successfully changed your flat name to {flate_name}!")
            else:
                st.warning("Please enter a new flat name")

    with st.expander("Roommates"):
        room_mate = st.text_input("Please enter the name of a roommate", key="new_room_mate_input")
        if st.button("Add new roommate"):
            if room_mate:  # Überprüfen, ob ein Name eingegeben wurde
                if room_mate not in st.session_state["roommates"]:  # Überprüfen, ob der Name nicht schon vorhanden ist
                    st.session_state["roommates"].append(room_mate)  # Speichere den Namen
                    st.success(f"Roommate {room_mate} has been added!")
                else:
                    st.warning(f"Roommate {room_mate} is already in the list!")

        if st.session_state["roommates"]:
            st.write("Current roommates:")
            for mate in st.session_state["roommates"]:
                st.write(f"- {mate}")

        roommate_to_remove = st.selectbox("Select a roommate to remove", st.session_state["roommates"])
        if st.button("Remove roommate"):
            if roommate_to_remove in st.session_state["roommates"]:
                st.session_state["roommates"].remove(roommate_to_remove)
                st.success(f"Roommate {roommate_to_remove} has been removed!")