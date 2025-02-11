import streamlit as st
import pandas as pd
import datetime

def calculate_hei(home_value, original_amount, multiplier, op_value, origination_date, 
                   purchase_date, premium_discount, investor_cap, appreciation, hold_period):
    contract_age = (purchase_date - origination_date).days // 30
    purchase_price = original_amount * (1 + premium_discount)
    sale_price = purchase_price * ((1 + appreciation) ** (hold_period / 12))
    
    results = {
        "Contract Age (Months)": contract_age,
        "Purchase Price": purchase_price,
        "Sale Price": sale_price,
    }
    return results

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
    results = calculate_hei(home_value, original_amount, multiplier, op_value, origination_date, 
                            purchase_date, premium_discount, investor_cap, appreciation, hold_period)
    st.write("### Results")
    st.write(results)
