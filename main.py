# streamlit_app.py
import streamlit as st
from streamlit_option_menu import option_menu
import Home, about, view_data, load_data, clean_data, visualize_data

# Use st.set_page_config to set the page title and icon
st.set_page_config (page_title="Automated EDA", page_icon="📊")


# Create a menu for selecting pages
page = option_menu(
    menu_title= None,
    options=["Home", "About", "Upload", "View", "Clean", "Viz"],
    icons=["house", "file-person-fill", "upload", "binoculars", "stars", "clipboard-data-fill"],
    menu_icon="cast",
    default_index=0,
    orientation= "horizontal"
)

# Display the selected page
if page == "Home":
    Home.show()

elif page == "About":
    about.show()

elif page == "Upload":
    load_data.show()

elif page == "View":
    view_data.show()

elif page == "Clean":
    clean_data.show()

elif page == "Visualize":
    visualize_data.show()
