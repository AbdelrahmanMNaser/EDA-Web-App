import streamlit as st
import pandas as pd

def show():
    st.header("Load Data")
    
    uploaded_file = st.file_uploader(label= "Upload a dataset", 
                                     type=["csv", "xlsx" , "xls", "xlsm", "xlsb", "ods" , "odt"], 
                                     label_visibility="collapsed"
                                    )

    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1]
        
        if file_extension == "csv":
            data = pd.read_csv(uploaded_file)
        elif file_extension in ["xlsx", "xls", "xlsm", "xlsb", "odf", "ods" , "odt"]:
            data = pd.read_excel(uploaded_file)
                   
        st.success("Data loaded successfully!")
             
        # Store the dataframe in st.session_state
        st.session_state.data = data
        st.session_state.name = uploaded_file.name