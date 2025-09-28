import streamlit as st
import pandas as pd
import sqlite3
import streamlit.components.v1 as components

#DATABASE CONNECTION
conn = sqlite3.connect("ola_rides.db")
 
# =========================
# CUSTOM STYLE (white + green theme)
# =========================
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #FFFFFF;
        color: #000000; /* Ensure default text color is black */
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #E8F5E9; /* light green */
    }

    /* === Headings - FIX for Visibility === */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important; /* Forces all standard headings to be black */
    }

    /* Target Streamlit's main heading elements */
    [data-testid="stHeader"] {
        background-color: #FFFFFF; /* Ensures the header background is white */
        color: #000000 !important; /* Sets header text to black */
    }
    
    /* Target elements used for st.title and st.header */
    .st-emotion-cache-10qbx9m, .st-emotion-cache-1pny2g, .st-emotion-cache-1cpxph, .st-emotion-cache-1215r66 {
        color: #000000 !important;
    }
    
    /* Target elements for all markdown text, including headings rendered via markdown */
    div.stMarkdown p {
        color: #000000 !important;
    }
    /* ===================================== */

    /* === Sidebar Label Fix === */
    /* Targets labels for selectboxes and other input widgets in the sidebar */
    .st-emotion-cache-10qbx9m p, /* This might cover some labels */
    .st-emotion-cache-v0k1vc, /* A common class for Streamlit labels */
    .st-emotion-cache-f1gq0z /* Another common class for Streamlit labels */
    {
        color: #000000 !important; /* Forces sidebar labels to be black */
    }
    
    /* More general target for text within the sidebar */
    section[data-testid="stSidebar"] .st-emotion-cache-10qbx9m,
    section[data-testid="stSidebar"] div[data-testid^="stVerticalBlock"] div[data-testid^="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] div[data-testid="stText"] p {
        color: #000000 !important;
    }

    /* ========================= */


    /* Dataframe table headers */
    .stDataFrame thead tr th {
        background-color: #000000 !important;  /* black */
        color: white !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #000000;  /* black */
        color: white;
        border-radius: 8px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #333333;  /* dark gray on hover */
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#STREAMLIT APP
st.set_page_config(page_title="OLA Ride Analytics", layout="wide")
st.title("TripTrends: Ola Ride Analytics")

# Sidebar filters
st.sidebar.header("Parameters")
vehicle_type = st.sidebar.multiselect("Vehicle Type", 
                                      options=pd.read_sql("SELECT DISTINCT Vehicle_Type FROM rides", conn)["Vehicle_Type"].tolist())
payment_method = st.sidebar.multiselect("Payment Method", 
                                        options=pd.read_sql("SELECT DISTINCT Payment_Method FROM rides", conn)["Payment_Method"].tolist())
booking_status = st.sidebar.multiselect("Booking Status", 
                                        options=pd.read_sql("SELECT DISTINCT Booking_Status FROM rides", conn)["Booking_Status"].tolist())

# Base query
query = "SELECT * FROM rides WHERE 1=1"
if vehicle_type:
    query += f" AND Vehicle_Type IN ({','.join(['?']*len(vehicle_type))})"
if payment_method:
    query += f" AND Payment_Method IN ({','.join(['?']*len(payment_method))})"
if booking_status:
    query += f" AND Booking_Status IN ({','.join(['?']*len(booking_status))})"

params = vehicle_type + payment_method + booking_status
df = pd.read_sql(query, conn, params=params)

st.subheader("Focused Rides Data")
st.dataframe(df, use_container_width=True)

# Predefined queries
st.subheader("Predefined SQL Queries")
queries = {
    "1. Successful Bookings": "SELECT * FROM rides WHERE Booking_Status = 'Success'",
    "2. Avg Ride Distance per Vehicle": "SELECT Vehicle_Type, AVG(Ride_Distance) as Avg_Distance FROM rides GROUP BY Vehicle_Type",
    "3. Cancelled Rides by Customers": "SELECT COUNT(*) AS Cancelled_By_Customers FROM rides WHERE Booking_Status = 'Canceled By Customer'",
    "4. Top 5 Customers by Ride Count": "SELECT Customer_ID, COUNT(*) AS Total_Rides FROM rides GROUP BY Customer_ID ORDER BY Total_Rides DESC LIMIT 5",
    "5. Driver Cancellations (Personal & Car issue)": "SELECT Canceled_Rides_by_Driver, COUNT(*) AS Total FROM rides WHERE Booking_Status = 'Canceled By Driver' AND Canceled_Rides_by_Driver = 'Personal & Car related issue' GROUP BY Canceled_Rides_by_Driver",
    "6. Max & Min Driver Rating for Prime Sedan": "SELECT MAX(Driver_Ratings) as Max_Rating, MIN(Driver_Ratings) as Min_Rating FROM rides WHERE Vehicle_Type = 'Prime Sedan'",
    "7. Rides Paid with UPI": "SELECT * FROM rides WHERE Payment_Method = 'UPI'",
    "8. Avg Customer Rating per Vehicle": "SELECT Vehicle_Type, AVG(Customer_Rating) as Avg_Rating FROM rides GROUP BY Vehicle_Type",
    "9. Total Booking Value (Successful)": "SELECT SUM(Booking_Value) as Total_Revenue FROM rides WHERE Booking_Status = 'Success'",
    "10. Incomplete Rides with Reason": "SELECT Booking_Status, Canceled_Rides_by_Driver FROM rides WHERE Booking_Status != 'Success'"
}

selected_query = st.selectbox("Choose a Query", list(queries.keys()))
result = pd.read_sql(queries[selected_query], conn)
st.dataframe(result, use_container_width=True)

#EMBED POWER BI
st.subheader("Power BI Visualization Board")

# Correct embedding
powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=6a97c615-abd2-4f9f-a265-c4bfa084e0bf&autoAuth=true&ctid=93f7ca22-f776-43cb-9efd-927d1c2f0603"
components.iframe(powerbi_url, width=1140, height=600)
