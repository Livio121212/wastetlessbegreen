import streamlit as st
import pandas as pd
from PIL import Image
import requests
from datetime import datetime
from settings_page import setup_flat_name, setup_roommates, add_roommate, display_roommates, settingspage, change_flat_name, manage_roommates, remove_roommate



# Initialization of session state variables
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
    st.session_state["expenses"] = {mate: 0.0 for mate in st.session_state["roommates"]}
if "purchases" not in st.session_state:
    st.session_state["purchases"] = {mate: [] for mate in st.session_state["roommates"]}
if "consumed" not in st.session_state:
    st.session_state["consumed"] = {mate: [] for mate in st.session_state["roommates"]}

# Ensure each roommate has initialized entries in expenses, purchases, and consumed
def ensure_roommate_entries():
    for mate in st.session_state["roommates"]:
        if mate not in st.session_state["expenses"]:
            st.session_state["expenses"][mate] = 0.0
        if mate not in st.session_state["purchases"]:
            st.session_state["purchases"][mate] = []
        if mate not in st.session_state["consumed"]:
            st.session_state["consumed"][mate] = []

# Function to change pages
def change_page(new_page):
    st.session_state["page"] = new_page

# Sidebar navigation with buttons
st.sidebar.title("Navigation")
if st.sidebar.button("Overview"):
    change_page("overview")
if st.sidebar.button("Fridge"):
    change_page("fridge")
if st.sidebar.button("Scan"):
    change_page("scan")
if st.sidebar.button("Recipes"):
    change_page("recipes")
if st.sidebar.button("Settings"):
    change_page("settings")

# Function for the overview page
def overview_page():
    title = f"Overview: {st.session_state['flate_name']}" if st.session_state["flate_name"] else "Overview"
    st.title(title)
    st.write("Welcome to the main page of your app.")
    st.write("Here you can display general information.")

# Function for the recipes page
def recipes_page():
    st.title("Recipes")
    st.write("This is the content of the Recipes page.")
    st.slider("Choose a value:", 0, 100, 50, key="slider_recipes")


def delete_product_from_inventory(food_item, quantity, unit, selected_roommate):
    ensure_roommate_entries()
    if selected_roommate not in st.session_state["consumed"]:
        st.session_state["consumed"][selected_roommate] = []
    delete_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if food_item and quantity > 0 and selected_roommate:
        if food_item in st.session_state["inventory"]:
            current_quantity = st.session_state["inventory"][food_item]["Quantity"]
            current_price = st.session_state["inventory"][food_item]["Price"]
            if quantity <= current_quantity:
                # Calculate the price per unit
                price_per_unit = current_price / current_quantity if current_quantity > 0 else 0
                amount_to_deduct = price_per_unit * quantity
                # Update inventory
                st.session_state["inventory"][food_item]["Quantity"] -= quantity
                st.session_state["inventory"][food_item]["Price"] -= amount_to_deduct
                st.session_state["expenses"][selected_roommate] -= amount_to_deduct
                st.success(f"'{quantity}' of '{food_item}' has been removed.")
                # Log the removal in consumed
                st.session_state["consumed"][selected_roommate].append({
                    "Product": food_item,
                    "Quantity": quantity,
                    "Price": amount_to_deduct,
                    "Unit": unit,
                    "Date": delete_time
                })
                # Remove item if quantity reaches zero
                if st.session_state["inventory"][food_item]["Quantity"] <= 0:
                    del st.session_state["inventory"][food_item]
            else:
                st.warning("The quantity to remove exceeds the available quantity.")
        else:
            st.warning("This item is not in the inventory.")
    else:
        st.warning("Please fill in all fields.")

# Function to add product to inventory
def add_product_to_inventory(food_item, quantity, unit, price, selected_roommate):
    ensure_roommate_entries()
    if selected_roommate not in st.session_state["expenses"]:
        st.session_state["expenses"][selected_roommate] = 0.0
    if selected_roommate not in st.session_state["purchases"]:
        st.session_state["purchases"][selected_roommate] = []
    purchase_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if food_item in st.session_state["inventory"]:
        st.session_state["inventory"][food_item]["Quantity"] += quantity
        st.session_state["inventory"][food_item]["Price"] += price
    else:
        st.session_state["inventory"][food_item] = {"Quantity": quantity, "Unit": unit, "Price": price}
    
    st.session_state["expenses"][selected_roommate] += price
    st.session_state["purchases"][selected_roommate].append({
        "Product": food_item,
        "Quantity": quantity,
        "Price": price,
        "Unit": unit,
        "Date": purchase_time
    })
    st.success(f"'{food_item}' has been added to the inventory, and {selected_roommate}'s expenses were updated.")

# Fridge page function
def fridge_page():
    ensure_roommate_entries()
    st.title("Fridge")

    # Roommate selection
    if st.session_state["roommates"]:
        selected_roommate = st.selectbox("Select the roommate:", st.session_state["roommates"])
    else:
        st.warning("No roommates available.")
        return

    # Action selection: Add or Remove
    action = st.selectbox("Would you like to add or remove an item?", ["Add", "Remove"])

    if action == "Add":
        # Input fields for food item, quantity, unit, and price
        food_item = st.text_input("Enter a food item to add:")
        quantity = st.number_input("Quantity:", min_value=0.0)
        unit = st.selectbox("Unit:", ["Pieces", "Liters", "Grams"])
        price = st.number_input("Price (in CHF):", min_value=0.0)

        # Button to add the food item
        if st.button("Add item"):
            if food_item and quantity > 0 and price >= 0 and selected_roommate:
                add_product_to_inventory(food_item, quantity, unit, price, selected_roommate)
            else:
                st.warning("Please fill in all fields.")
    
    elif action == "Remove":
        # Select the item to remove
        if st.session_state["inventory"]:
            food_item = st.selectbox("Select a food item to remove:", list(st.session_state["inventory"].keys()))
            quantity = st.number_input("Quantity to remove:", min_value=1.0, step=1.0)
            unit = st.session_state["inventory"][food_item]["Unit"]

            # Button to remove the item
            if st.button("Remove item"):
                delete_product_from_inventory(food_item, quantity, unit, selected_roommate)
        else:
            st.warning("The inventory is empty.")

    # Display current inventory
    if st.session_state["inventory"]:
        st.write("Current Inventory:")
        inventory_df = pd.DataFrame.from_dict(st.session_state["inventory"], orient='index')
        inventory_df = inventory_df.reset_index().rename(columns={'index': 'Food Item'})
        st.table(inventory_df)
    else:
        st.write("The inventory is empty.")

    # Display total expenses per roommate
    st.write("Total expenses per roommate:")
    expenses_df = pd.DataFrame(list(st.session_state["expenses"].items()), columns=["Roommate", "Total Expenses (CHF)"])
    st.table(expenses_df)

    # Display purchases and consumed items per roommate
    st.write("Purchases and Consumptions per roommate:")
    for mate in st.session_state["roommates"]:
        st.write(f"**{mate}'s Purchases:**")
        purchases_df = pd.DataFrame(st.session_state["purchases"][mate])
        st.table(purchases_df)

        st.write(f"**{mate}'s Consumptions:**")
        consumed_df = pd.DataFrame(st.session_state["consumed"][mate])
        st.table(consumed_df)

# Barcode dekodieren
def decode_barcode(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode("utf-8")
    return None

# Produktinformationen abrufen
def get_product_info(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            product = data["product"]
            return {
                "name": product.get("product_name", "Unknown Product"),
                "brand": product.get("brands", "Unknown Brand")
            }
    return None
# Gesamtausgaben anzeigen
def display_total_expenses():
    with st.expander("View Total Expenses per Roommate"):
        expenses_df = pd.DataFrame(list(st.session_state["expenses"].items()), columns=["Roommate", "Total Expenses (CHF)"])
        st.table(expenses_df)

# Einkäufe anzeigen
def display_purchases():
    with st.expander("Purchases per Roommate"):
        for roommate, purchases in st.session_state["purchases"].items():
            st.write(f"**{roommate}**")
            if purchases:
                purchases_df = pd.DataFrame(purchases)
                st.table(purchases_df)
            else:
                st.write("No purchases recorded.")

def barcode_page():
    st.title("Upload your barcode")
    uploaded_file = st.file_uploader("Upload an image with a barcode", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.write("Scanning for barcode...")
        barcode = decode_barcode(image)

        if barcode:
            st.write(f"Barcode found: {barcode}")
            st.write("Looking up product information...")
            product_info = get_product_info(barcode)

            if product_info:
                food_item = st.text_input("Product:", value=product_info['name'])
                brand = st.text_input("Brand:", value=product_info['brand'])
            else:
                st.write("Product not found in database.")
                food_item = st.text_input("Product:")
                brand = st.text_input("Brand:")

            selected_roommate = st.selectbox("Who bought the product?", st.session_state["roommates"])
            quantity = st.number_input("Quantity:", min_value=0.0, step=0.1, format="%.2f")
            unit = st.selectbox("Unit:", ["Pieces", "Liters", "Grams"])
            price = st.number_input("Price (in CHF):", min_value=0.0, step=0.1, format="%.2f")

            if st.button("Add product to inventory"):
                if food_item and quantity > 0 and price >= 0:
                    add_product_to_inventory(food_item, quantity, unit, price, selected_roommate)
                else:
                    st.warning("Please fill in all fields.")
        else:
            st.write("No barcode found in the image.")

    display_total_expenses()
    display_purchases()               

# Page display logic for the selected page
if st.session_state["page"] == "overview":
    overview_page()
elif st.session_state["page"] == "fridge":
    fridge_page()
elif st.session_state["page"] == "scan":
    barcode_page()
elif st.session_state["page"] == "recipes":
    recipes_page()
elif st.session_state["page"] == "settings":
    if not st.session_state["setup_finished"]:
        if st.session_state["flate_name"] == "":
            setup_flat_name()
        else:
            setup_roommates()
    else:
        settingspage()