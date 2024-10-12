import streamlit as st
import pandas as pd
def currStock(connection):
    st.title("Current Stock")

    # Fetch and display current stock
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM pharmacy_inventory WHERE quantity > 0")
    # stock = cursor.fetchall()

    if 0:
        df = pd.DataFrame(None, columns=['ID', 'Medicine Name', 'Quantity', 'Expiry Date'])
        st.table(df)
    else:
        st.info("No medicines in stock.")