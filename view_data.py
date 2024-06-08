import pandas as pd
import streamlit as st


def display_dataframe(df):
    
    df_display_options = st.sidebar.radio(label="Display Options", options= ["All", "Top"]) 

    if df_display_options == "All":
        st.dataframe(df)

    elif df_display_options == "Top":
        st.dataframe(df.head(25))


def show():
    if "data" in st.session_state:
        df = st.session_state.data

        st.write(st.session_state.name)
        st.header("View Data")

        display_dataframe(df)
        st.write("\t")

        col1, col2 = st.columns(2)

        with col1:
            
            st.write(df.dtypes)

        with col2:
            st.write(df.describe(include= "all"))

    else:
        st.error("No Dataset is Uploaded")
                    