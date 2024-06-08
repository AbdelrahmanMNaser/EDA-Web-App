import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def handle_missing_values(df, mode, num_cols, cat_cols, missing_cols):
    if mode == "--Select--":
        st.dataframe(df[df.isna().any(axis = 1)])
                

    elif mode == "Manual":
        st.sidebar.header("Choose a column with missing values")
        col = st.sidebar.selectbox("Column", options=missing_cols, key="col")
        st.sidebar.text(
            f"""
            Missing values: {df[col].isna().sum()}\n
            Total values: {df.shape[0]}\n
            Percentage: {np.round(df[col].isna().sum() / df.shape[0] * 100)}%
            """
            )
        
        if col in num_cols:            
            st.dataframe(df[df[col].isna()])

            option = st.sidebar.selectbox(label=f"How do you want to handle \"{col}\"?", 
                                        options=["--Select--", "Drop", "Fill"], 
                                        key="option"
                                        )
            
            if option == "--Select--":
                pass

            elif option == "Drop":
                method = st.sidebar.radio(label="What do you want to drop?", 
                                        options=["--Select--", "Drop rows", f"Drop column \"{col}\""], 
                                        key="method"
                                        )
                st.session_state.handling_method[col] = (option, method)
            
            elif option == "Fill":
                method = st.sidebar.radio(label=f"How do you want to fill \"{col}\"?", 
                                        options=["Mean", "Median", "Mode"], 
                                        key="method"
                                        )
                st.session_state.handling_method[col] = (option, method)

        elif col in cat_cols:
            st.dataframe(df[df[col].isna()])
            option = st.sidebar.selectbox(label=f"How do you want to handle \"{col}\"?", 
                                        options=["--Select--", "Drop", "Fill"], 
                                        key="option"
                                        )
            
            if option == "--Select--":
                pass
            
            elif option == "Drop":
                method = st.sidebar.radio(label="What do you want to drop?", 
                                        options=["--Select--", "Drop rows", f"Drop column \"{col}\""], 
                                        key="method"
                                        )
                st.session_state.handling_method[col] = (option, method)
            
            elif option == "Fill":
                method = st.sidebar.radio(label=f"How do you want to fill \"{col}\"?", 
                                        options=["Mode"], 
                                        key="method"
                                        )
                st.session_state.handling_method[col] = (option, method)
        
        apply_missing = st.sidebar.button("Apply Handling")

        if apply_missing:
            for col, method in st.session_state.handling_method.items():          
            
                if method[0] == "--Select--":
                    continue
                
                elif method[0] == "Drop":

                    if method[1] == "--Select--":
                        continue
                    
                    elif method[1] == "Drop rows":
                        df.dropna(subset=[col], inplace=True)
                        
                        if col in num_cols:    
                            num_cols.remove(col)
                        
                        elif col in cat_cols:
                            cat_cols.remove(col)
                        
                    elif method[1] == f"Drop column \"{col}\"":
                        df.drop(col, axis="columns", inplace=True)
                        
                        if col in num_cols:
                            num_cols.remove(col)

                        elif col in cat_cols:
                            cat_cols.remove(col)
                    
                elif method[0] == "Fill":
                    if col in num_cols:

                        if method[1] == "Mean":
                            df[col].fillna(df[col].mean(), inplace=True)

                        elif method[1] == "Median":
                            df[col].fillna(df[col].median(), inplace=True)

                        elif method[1] == "Mode":
                            df[col].fillna(df[col].mode()[0], inplace=True)
                        
                    elif col in cat_cols:                        
                        if method[1] == "Mode":
                            df[col].fillna(df[col].mode()[0], inplace=True)
            

    elif mode == "Auto":
        
        st.sidebar.subheader("Filling Method")
        fill_method_num = st.sidebar.selectbox(label="Numerical columns", 
                                                options=["--Select--", "Mean", "Median", "Mode", "Zeroes"], 
                                                key="fill_method_num"
                                                )
                
        fill_method_cat = st.sidebar.selectbox(label="Categorical columns", 
                                                options=["--Select--","Mode", "NaN"], 
                                                key="fill_method_cat"
                                                )
                    
        st.sidebar.subheader("Drop Method")
        min_percentage_rows = st.sidebar.number_input(label="Minimum percentage of missing values to Drop rows", 
                                                        min_value=0,
                                                        max_value=100,
                                                        step=5, 
                                                        key="min_percentage_rows"
                                                        )
        
        min_percentage_cols = st.sidebar.number_input(label="Minimum percentage of missing values to Drop columns", 
                                                        min_value=min_percentage_rows + 20,
                                                        max_value=100,
                                                        step=5, 
                                                        key="min_percentage_cols"
                                                        )
                    
        apply = st.sidebar.button(label="Apply changes", key="apply")
        
        if apply:
            for col in missing_cols:
                percentage = np.round(df[col].isna().sum() / df.shape[0] * 100)
                if percentage > min_percentage_rows:

                    if percentage > min_percentage_cols:
                        df.drop(col, axis="columns", inplace=True)
                        cat_cols.remove(col)

                    else:
                        df.dropna(subset=[col], inplace=True)
                        num_cols.remove(col)                                    
                                    
                else:
                    if col in num_cols:

                        if fill_method_num == "--Select--":
                            pass

                        elif fill_method_num == "Mean":
                            df[col].fillna(df[col].mean(), inplace=True)

                        elif fill_method_num == "Median":
                            df[col].fillna(df[col].median(), inplace=True)

                        elif fill_method_num == "Mode":
                            df[col].fillna(df[col].mode()[0], inplace=True)
                        
                        elif fill_method_num == "Zeroes":
                            df[col].fillna(0, inplace=True)

                    elif col in cat_cols:

                        if fill_method_cat == "--Select--":
                            pass

                        elif fill_method_cat == "Mode":
                            df[col].fillna(df[col].mode()[0], inplace=True)
                        
                        elif fill_method_cat == "NaN":
                            df[col].fillna(np.nan, inplace=True)
            
            st.sidebar.success("Changes applied successfully!")  
            st.write("Updated dataframe:")
            st.dataframe(df[df.isna().any(axis = 1)])

def remove_outliers_iqr(df, outlier_cols):
    # Ensure 'outlier_cols' is a list of column names
    assert isinstance(outlier_cols, list), "outlier_cols must be a list of column names"

    if not outlier_cols:
        return df, outlier_cols

    # Select a column to analyze for outliers
    col = st.sidebar.selectbox(label="Column", options=outlier_cols, key="outlier_col")

    # Calculate the 25th and 75th percentiles
    percentile25 = df[col].quantile(0.25)
    percentile75 = df[col].quantile(0.75)

    # Calculate the interquartile range (IQR)
    iqr = percentile75 - percentile25

    # Define the upper and lower limits for detecting outliers
    upper_limit = percentile75 + 1.5 * iqr
    lower_limit = percentile25 - 1.5 * iqr

    # Identify the outliers
    upper_outliers = df[col] > upper_limit
    lower_outliers = df[col] < lower_limit

    # Display boxplot before removing outliers
    col1, col2 = st.columns(2)
    with col1:
        st.write("Before Handling")
        st.plotly_chart(px.box(df, y=col), use_container_width=True)

    # Create checkboxes for user to select which outliers to remove
    remove_upper = st.sidebar.checkbox("Remove Upper Outliers", key=f"{col}_upper")
    remove_lower = st.sidebar.checkbox("Remove Lower Outliers", key=f"{col}_lower")

    # Button to apply the selected outlier handling methods
    apply_outliers = st.sidebar.button("Apply Outlier Handling")

    if apply_outliers:
        # Remove or replace outliers based on user selection
        if remove_upper:
            df = df[~upper_outliers]
        if remove_lower:
            df = df[~lower_outliers]

        # Save the modified dataframe back to st.session_state
        st.session_state.data = df

        # Update the boxplot after removing outliers
        with col2:
            st.write("After Handling")
            st.plotly_chart(px.box(df, y=col), use_container_width=True)

        # Update the list of columns in the selectbox
        # Make sure to handle the case where the column list is empty
        if col in outlier_cols:
            outlier_cols.remove(col)
            st.session_state.outlier_cols = outlier_cols 

    if not outlier_cols:
        st.info("No Outliers")


    return df, outlier_cols



def show():
    if "data" in st.session_state:    
        df = st.session_state.data    

        st.write(st.session_state.name)
        st.header("Clean Data")

        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(exclude="number").columns.tolist()

        handling_menu = st.sidebar.selectbox("What do you Want to Handle:",
                                             options=["--Select--", "Missing Values", "Outliers"],
                                             key="handling_menu"
        )

        if handling_menu == "--Select--":
            pass

        elif handling_menu == "Missing Values":                
                

            missing_cols = df.columns[df.isna().any()].tolist()
            print(missing_cols)

            if missing_cols:            
                st.sidebar.header("Handling missing values")

                if "handling_method" not in st.session_state:
                    st.session_state.handling_method = {}
                
                mode = st.sidebar.selectbox("Choose Handling mode", 
                                            options=["--Select--", "Manual", "Auto"], 
                                            key="mode"
                                            )
                
                handle_missing_values(df, mode, num_cols, cat_cols, missing_cols)
            
            else:
                st.info("No Missing Values")

        elif handling_menu == "Outliers":
            outlier_cols = []
            print(outlier_cols)

            # Loop over the numeric columns
            for col in num_cols:
                if df[col].mean() > df[col].median():
                    outlier_cols.append(col)

            if "outlier_cols" not in st.session_state:
                st.session_state.outlier_cols = outlier_cols

            if st.session_state.outlier_cols:
                outlier_handling = st.sidebar.selectbox(label= "Handle Outlier",
                                                            options= ["--Select--", "IQR"]
                                                            )
                    
                if outlier_handling == "--Select--":
                    pass

                elif outlier_handling == "IQR":
                    df, outlier_cols = remove_outliers_iqr(st.session_state.data, st.session_state.outlier_cols)
            
            else:
                st.info("No outliers")
    
    else:
        st.error("No Dataset is uploaded")
