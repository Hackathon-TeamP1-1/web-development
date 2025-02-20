import streamlit as st

def show_sidebar():
    """Display a permanently fixed sidebar under the header with items aligned at the top."""

    st.markdown("""
        <style>
            /* Sidebar Positioned Below Header */
            section[data-testid="stSidebar"] {
                position: fixed;
                top: 61px; /* Adjusted for spacing below header */
                left: 0;
                width: 250px;
                height: calc(100vh - 60px);
                background-color: #FFFFFF; /* White Sidebar */
                padding: 15px;
                overflow-y: auto;
                border-right: 1px solid #E0E0E0; /* Light border */
                display: flex;
                flex-direction: column;
                align-items: flex-start; /* Align items to the top */
                justify-content: flex-start; /* Move content to the top */
            }

            section[data-testid="stSidebar"] * {
                color: #000000 !important; /* Black text */
                font-size: 16px !important;
            }

            /* Sidebar Header Styling */
            .stSidebarContent h2 {
                font-size: 18px !important;
                font-weight: bold !important;
                color: #333333 !important;
                padding-bottom: 10px;
            }

            /* Move Sidebar Items to the Top */
            .stSidebarContent {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                justify-content: flex-start;
            }

            /* Adjust Sidebar Select Boxes */
            .stSelectbox {
                background-color: #F5F5F5 !important; /* Light background */
                border-radius: 5px !important;
                padding: 8px;
                width: 100%;
                margin-bottom: 10px; /* Space between elements */
            }

        </style>
    """, unsafe_allow_html=True)

    # Sidebar Filters
    st.sidebar.header("📊 Climate Data Selection")

    climate_variable = st.sidebar.selectbox(
        "Choose a Climate Variable",
        ["Temperature", "Wind Speed", "UV Index", "Solar Radiation"]
    )

    city_choice = st.sidebar.selectbox(
        "Choose a City",
        ["All Palestine", "Gaza", "Jericho", "Hebron", "Tulkarm", "Jenin" ,"Qalqilya" ,"Bethlehem", "Ramallah", "Rafah", "Khan Younis"],
        index=0  # Default selection is "All Palestine"
    )

    return climate_variable, city_choice
