def overview_page():
    # Sets the title to "Overview: Name of the flat"
    title = f"Overview: {st.session_state['flate_name']}" if st.session_state["flate_name"] else "Overview"
    st.title(title)
    st.write("Welcome to the main page of your app.")
    st.write("Here you can display general information.")