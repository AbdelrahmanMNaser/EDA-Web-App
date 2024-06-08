import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def Univariate(df, num_cols, cat_cols):
    st.sidebar.header("Choose a column to visualize")

    col = st.sidebar.selectbox(label= "Select a column", options= df.columns)

    if col in num_cols:   
        left_co, cent_co,last_co = st.columns(3)

        with cent_co:
           st.write(df[col].value_counts())

        graph_types = ["Histogram" , "Box Plot"]

        for i, graph_type in enumerate(graph_types):
            checked = st.sidebar.checkbox(graph_type, key= col+graph_type)
            
            if checked:
                st.subheader(f"{graph_type} for \"{col}\"")

                if graph_type == "Histogram":
                    nbins = st.slider(label="Select number of bins" , min_value= 5 , max_value= 50 , step= 5)
                    fig = px.histogram(data_frame= df , x = col, text_auto=True , nbins=nbins )
                    fig.update_layout(bargap = 0.1)
                    fig.update_traces(textposition = "outside" , textfont_size = 15)
                    st.plotly_chart(fig)
                
                elif graph_type == "Box Plot":
                    fig = px.box(data_frame= df , y = col)
                    st.plotly_chart(fig)

    elif col in cat_cols:

        col_count = df[col].value_counts()
        percentages = df[col].value_counts(normalize = True) * 100

        method = st.sidebar.radio(label= "Choose Selection Method" , 
                                    options=["All" , "Percentage" , "Top"]
                                )

        if method == "All":
            pass
        
        elif method == "Percentage":
            minimum_percentage = st.sidebar.number_input(label= "Enter Minimum Percentage: ", 
                                                        min_value=1 , 
                                                        max_value=100 , 
                                                        step=1,
                                                        key= col+"minimum_percentage"
                                                    )

            def filter_func(x): 
                return x / col_count.sum() > minimum_percentage/100
            
            col_count = col_count[col_count.apply(filter_func)]

        elif method == "Top":
            top_selection = st.sidebar.number_input("Enter: " , min_value=1 , max_value= df.shape[0] , step=1)
            col_count = col_count.head(top_selection)

        left_co, cent_co,last_co = st.columns(3)
        
        with cent_co:
           st.write(col_count)

        graph_types = ["Bar Plot" , "Pie Chart"]

        for i, graph_type in enumerate(graph_types):
            checked = st.sidebar.checkbox(graph_type, key= col+graph_type)
            
            if checked:
                st.subheader(f"{graph_type} for \"{col}\"")

                if graph_type == "Bar Plot":
                    fig = px.bar(
                        data_frame=col_count,
                        x=col_count.index, 
                        y="count", 
                        height=576 , 
                        width= 760 , 
                        text= "count" , 
                        color= col_count.index
                        )
                    fig.update_traces(textposition = "outside")
                    fig.update_layout(uniformtext_minsize = 10)
                    st.plotly_chart(fig)
                
                elif graph_type == "Pie Chart":
                    fig = px.pie(
                        data_frame= col_count,
                        values= col_count.values,
                        names= col_count.index
                        )
                    fig.update_layout(width=760, height=520)
                    fig.update_layout({'font': {'size': 18}, })
                    fig.update_traces(textposition = 'inside' , textinfo = 'label+percent')
                    st.plotly_chart(fig)

def Bivariate(df, num_cols, cat_cols):
    same_size_numcols = []

    for col in num_cols :
        if df[col].size == df.shape[0]:
            same_size_numcols.append(col)

    same_size_catcols = []

    for col in cat_cols:
        if df[col].size == df.shape[0]:
            same_size_catcols.append(col)

    same_size_cols = same_size_numcols + same_size_catcols
    
    x_axis = st.sidebar.selectbox(label= "X-axis" , options= same_size_cols)     
    x_axis_count = df[x_axis].value_counts()

    switch_variables = st.sidebar.button(label="Switch", key="swtch_var")
    
    y_axis = st.sidebar.selectbox(label= "Y-axis" ,options= df.columns)    
    y_axis_count = df[y_axis].value_counts()
    
    if switch_variables:
        x_axis, y_axis = y_axis, x_axis
        x_axis_count = df[x_axis].value_counts()
        y_axis_count = df[y_axis].value_counts()


    crossed = pd.crosstab(index= df[x_axis] , columns= df[y_axis])

    if x_axis in cat_cols: 


        method = st.sidebar.radio(label= f"Choose Selection Method for \"{x_axis}\" " , 
                                    options=["All" , "Percentage" , "Top"],
                                    key= "x_axis selection"
                                    )

        if method == "All":
            pass
        
        elif method == "Percentage":    
            x_axis_percentages = df[x_axis].value_counts(normalize = True) * 100
            
            min_percentage = st.sidebar.number_input(label= "Enter Minimum Percentage: ", 
                                                     min_value=1 , 
                                                     max_value=100 , 
                                                     step=1,
                                                     key= "x_axis min percentage"
                                                    )

            def filter_func(x): 
                return x / x_axis_count.sum() > min_percentage/100
            
            x_axis_count = x_axis_count[x_axis_count.apply(filter_func)]

        elif method == "Top":
            top_selection = st.sidebar.number_input(label= "Enter: " , 
                                                    min_value=1 , 
                                                    max_value= df.shape[0] , 
                                                    step=1,
                                                    key= "x_axis top selection"
                                                    )
            
            x_axis_count = x_axis_count.head(top_selection)

    if y_axis in cat_cols:

        method = st.sidebar.radio(label= f"Choose Selection Method for \" {y_axis}\"" , 
                                    options= ["All" , "Percentage" , "Top"],
                                    key= "y_axis selection"
                                    )

        if method == "All":
            pass
        
        elif method == "Percentage":        
            y_axis_percentages = df[y_axis].value_counts(normalize = True) * 100

            min_percentage = st.sidebar.number_input(label= "Enter Minimum Percentage  : ", 
                                                     min_value=1 , 
                                                     max_value=100 , 
                                                     step=1,
                                                     key= "y_axis min percentage"
                                                    )

            def filter_func(x): 
                return x / y_axis_count.sum() > min_percentage/100
            
            y_axis_count = y_axis_count[y_axis_count.apply(filter_func)]

        elif method == "Top":
            top_selection = st.sidebar.number_input(label= "Enter: ", 
                                                    min_value=1 , 
                                                    max_value= df.shape[0] , 
                                                    step=1,
                                                    key= "y_axis top selection"
                                                    )
            y_axis_count = y_axis_count.head(top_selection)


    df_x = df.loc[df[x_axis].isin(x_axis_count.index)]

    df_y = df.loc[df[y_axis].isin(y_axis_count.index)]

    crossed = pd.crosstab(index=df_x[x_axis], columns=df_y[y_axis])
    
    left_co, cent_co,last_co = st.columns(3)
        
    with cent_co:
        st.write(crossed)
    
    if x_axis in num_cols:
        graph_types = ["Bar Plot" , "Box Plot", "Line Chart" , "Scatter Plot"]

        for i, graph_type in enumerate(graph_types):
            checked = st.sidebar.checkbox(graph_type)
            
            if checked:
                st.subheader(f"{graph_type} for relation between \"{x_axis}\" & \"{y_axis}\"")

                if graph_type == "Bar Plot":
                    fig = px.bar(data_frame= crossed , barmode="group", text_auto=True)
                    fig.update_traces(textposition = "outside")
                    fig.update_layout(uniformtext_minsize = 10)
                    st.plotly_chart(fig)
                
                elif graph_type == "Box Plot":
                    fig = px.box(data_frame= crossed)
                    st.plotly_chart(fig)

                elif graph_type == "Line Chart":
                    fig = px.line(data_frame=crossed)
                    st.plotly_chart(fig)

                elif graph_type == "Scatter Plot":
                    fig = px.scatter(data_frame= crossed, symbol= y_axis)
                    st.plotly_chart(fig)


    elif x_axis in cat_cols: 
        graph_types = ["Bar Plot", "Box Plot"]

        for i, graph_type in enumerate(graph_types):
            checked = st.sidebar.checkbox(graph_type)
            
            if checked:
                st.subheader(f"{graph_type} for relation between \"{x_axis}\" & \"{y_axis}\"")

                if graph_type == "Bar Plot":            
                    bar_chart = px.bar(data_frame= crossed, barmode= "group")
                    bar_chart.update_traces(textposition = "outside")
                    bar_chart.update_layout(uniformtext_minsize = 10)
                    st.plotly_chart(bar_chart)

                elif graph_type == "Box Plot":
                    fig = px.box(data_frame= crossed)
                    st.plotly_chart(fig)

def show():    
    if "data" in st.session_state:
        df = st.session_state.data

        st.write(st.session_state.name)
        st.header("Visualize Data")

        st.sidebar.header("Choose a column to visualize")
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(exclude="number").columns.tolist()

        analysis_method = st.sidebar.selectbox(label= "Select Type of Analysis" ,
                                               options= [ "--Select--" , "Univariate Analysis" , "Bivariate Analaysis"])

        if analysis_method == "--Select--":
            pass

        elif analysis_method == "Univariate Analysis":
            Univariate(df, num_cols, cat_cols)   
            
        elif analysis_method == "Bivariate Analaysis":
            Bivariate(df, num_cols, cat_cols)    

    else:
        st.error("No Dataset is Uploaded")
    