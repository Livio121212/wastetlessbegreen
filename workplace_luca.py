import streamlit as st
import requests

# API-Key für Spoonacular
API_KEY = '21c590f808c74caabbaa1494c6196e7a'
SPOONACULAR_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# Erste Seite: WG-Daten eingeben
def wg_setup():
    st.title("🏠 Wasteless App - Setup")
    
    # WG Name eingeben
    wg_name = st.text_input("Enter your WG name:")
    roommates = st.text_area("Enter names of roommates (comma-separated):")

    if st.button("Save WG Details"):
        if wg_name and roommates:
            st.session_state.wg_name = wg_name
            st.session_state.roommates = [name.strip() for name in roommates.split(',')]
            st.success("WG details saved! Click the button below to proceed.")
            st.session_state.page = "inventory"
        else:
            st.error("Please fill in all fields.")

# Zweite Seite: Inventar und Rezepte
def inventory_and_recipes():
    st.title(f"🏠 {st.session_state.wg_name} Inventory and Recipes")
    
    # WG Mitglieder anzeigen
    st.subheader("👥 Roommates:")
    for roommate in st.session_state.roommates:
        st.write(f"- {roommate}")

    # Inventar initialisieren
    if 'inventory' not in st.session_state:
        st.session_state.inventory = []

    # WG Inventar hinzufügen
    st.header("🛒 Add Inventory Items")
    new_inventory_item = st.text_input("Add an item to the inventory:")
    item_amount = st.number_input("Enter the amount spent (CHF):", min_value=0.0)

    if st.button("Add Inventory Item"):
        if new_inventory_item and item_amount >= 0:
            st.session_state.inventory.append({'item': new_inventory_item, 'amount': item_amount})
            st.success(f"{new_inventory_item} has been added to the inventory with a cost of {item_amount:.2f} CHF!")

    # Zeige das Inventar an
    st.subheader("🛒 Inventory:")
    if st.session_state.inventory:
        for entry in st.session_state.inventory:
            st.write(f"- {entry['item']} (Cost: {entry['amount']:.2f} CHF)")
    else:
        st.write("No inventory items added.")

    # Rezepte suchen
    st.header("🍽️ Find Recipes")
    if st.button("Get Recipes"):
        if st.session_state.inventory:
            ingredients = [entry['item'] for entry in st.session_state.inventory]
            recipes = get_recipes(ingredients)
            if recipes:
                st.subheader("Found Recipes:")
                for recipe in recipes:
                    st.write(f"- **{recipe['title']}** (Link: [View Recipe](https://spoonacular.com/recipes/{recipe['id']}))")
            else:
                st.write("No recipes found with these ingredients.")
        else:
            st.warning("Please add inventory items first to find recipes.")

# Rezepte von Spoonacular abrufen
def get_recipes(ingredients):
    params = {
        'ingredients': ','.join(ingredients),
        'number': 5,
        'apiKey': API_KEY
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    return response.json() if response.status_code == 200 else []

# Seitenverwaltung
if 'page' not in st.session_state:
    st.session_state.page = "setup"

if st.session_state.page == "setup":
    wg_setup()
else:
    inventory_and_recipes()
