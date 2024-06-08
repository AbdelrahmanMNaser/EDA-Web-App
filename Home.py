import streamlit as st

def show():
    st.title("📌 Welcome to EDA App! 📌")

    st.markdown("This application is designed to make Exploratory Data Analysis (EDA) as seamless as possible. Here's what you can do:")

    st.markdown ("-  **📤 Upload:** Begin by uploading your CSV or EXCEL file. The app will read the data and prepare it for analysis.")
    st.markdown ("-  **🔍 View:** Once your data is uploaded, you can view it directly in the app. Get a feel for your dataset and identify any potential issues that need to be addressed.")
    st.markdown ("-  **🧹 Clean:** Our app provides options to handle missing values and outliers. With just a click, you can clean your data and make it ready for further analysis.")
    st.markdown ("- **📊 Visualize:** Finally, visualize your data with our built-in tools. Uncover patterns, trends, and insights that can guide your next steps.")

    col1, col2, col3 = st.columns(3)
    
    with col3:
        st.write("**Happy Analysis!** 🚀")