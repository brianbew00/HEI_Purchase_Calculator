import streamlit as st
import pandas as pd
import datetime

def calculate_hei(home_value, appreciation, origination_date, hold_period):
    data = []
    current_date = origination_date
    current_value = home_value
    
    for month in range(hold_period + 1):
        data.append([current_date, month, current_value])
        current_date += pd.DateOffset(months=1)
        current_value *= (1 + appreciation / 12)
    
    df = pd.DataFrame(data, columns=["Date", "Month", "Home Value"])
    return df

st.title("Home Equity Investment Simulator")

home_value = st.number_input("Home Value ($)", value=1000000.0, step=1000.0)
original_amount = st.number_input("Original Amount ($)", value=200000.0, step=1000.0)
multiplier = st.number_input("Multiplier", value=2.0, step=0.1)
op_value = st.number_input("Op Value", value=0.4, step=0.01)
origination_date = st.date_input("Origination Date", value=datetime.date(2023, 12, 11))
purchase_date = st.date_input("Purchase Date", value=datetime.date(2024, 2, 24))
premium_discount = st.number_input("Premium / Discount", value=0.06, step=0.01)
investor_cap = st.number_input("Investor Cap", value=0.2, step=0.01)
appreciation = st.number_input("Appreciation Rate (Annual)", value=0.03, step=0.01)
hold_period = st.number_input("Hold Period (Months)", value=12, step=1)

if st.button("Calculate"):
    df = calculate_hei(home_value, appreciation, origination_date, hold_period)
    st.write("### Home Value Over Time")
    st.dataframe(df)
