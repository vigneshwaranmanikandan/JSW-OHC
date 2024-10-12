import streamlit as st
import pandas as pd
def expiry(connection):
    st.title("Medicines Approaching Expiry")
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM pharmacy_inventory WHERE expiry_date <= CURDATE() + INTERVAL 30 DAY")
    # expiring_medicines = cursor.fetchall()

    if 0:
        df = pd.DataFrame(None, columns=['ID', 'Medicine Name', 'Quantity', 'Expiry Date'])
        st.table(df)
    else:
        st.info("No medicines are approaching expiry.")