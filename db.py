import sqlite3
import pandas as pd

#Load dataset
file_path = "OLA_Cleaned.xlsx"   
df = pd.read_excel(file_path)

#Connect to SQLite database
conn = sqlite3.connect("ola_rides.db")
cursor = conn.cursor()

#Save dataframe to SQL table
df.to_sql("rides", conn, if_exists="replace", index=False)

#Run SQL queries

#1. Retrieve all successful bookings
q1 = "SELECT * FROM rides WHERE Booking_Status = 'Success'"

#2. Find the average ride distance for each vehicle type
q2 = "SELECT Vehicle_Type, AVG(Ride_Distance) AS Avg_Distance FROM rides GROUP BY Vehicle_Type"

#3. Get the total number of cancelled rides by customers
q3 = "SELECT COUNT(*) AS Cancelled_By_Customers FROM rides WHERE Booking_Status = 'Cancelled by Customer'"

#4. List the top 5 customers who booked the highest number of rides
q4 = """SELECT Customer_ID, COUNT(*) AS Total_Rides 
        FROM rides 
        GROUP BY Customer_ID 
        ORDER BY Total_Rides DESC 
        LIMIT 5"""

#5. Get the number of rides cancelled by drivers due to personal and car-related issues
q5 = """SELECT Canceled_Rides_by_Driver, COUNT(*) AS Total
        FROM rides 
        WHERE Booking_Status = 'Canceled By Driver'
        AND Canceled_Rides_by_Driver = 'Personal & Car related issue'
        GROUP BY Canceled_Rides_by_Driver"""
#6. Find the maximum and minimum driver ratings for Prime Sedan bookings
q6 = """SELECT MAX(Driver_Ratings) AS Max_Rating, 
               MIN(Driver_Ratings) AS Min_Rating 
        FROM rides 
        WHERE Vehicle_Type = 'Prime Sedan'"""

#7. Retrieve all rides where payment was made using UPI
q7 = "SELECT * FROM rides WHERE Payment_Method = 'UPI'"

#8. Find the average customer rating per vehicle type
q8 = "SELECT Vehicle_Type, AVG(Customer_Rating) AS Avg_Rating FROM rides GROUP BY Vehicle_Type"

#9. Calculate the total booking value of rides completed successfully
q9 = "SELECT SUM(Booking_Value) AS Total_Revenue FROM rides WHERE Booking_Status = 'Success'"

#10. List all incomplete rides along with the reason
q10 = "SELECT * FROM rides WHERE Booking_Status != 'Success'"

#Execute and display results
queries = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
for i, q in enumerate(queries, 1):
    print(f"\nQuery {i} Results:")
    result = pd.read_sql(q, conn)
    print(result.head(10))  # show first 10 rows for preview

#Close connection
conn.close()



