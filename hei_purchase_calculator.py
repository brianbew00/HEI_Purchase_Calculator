import streamlit as st
import pandas as pd
import datetime

def calculate_forecast(home_value, appreciation, origination_date, months=120):
    """
    Forecast the home’s value month-by-month using monthly compounding.
    Returns a DataFrame with the index labeled as "Month", and columns for Date and Forecasted HEI Value.
    """
    data = []
    current_value = home_value
    current_date = pd.to_datetime(origination_date)
    
    # Forecast for each month from 0 to months (inclusive)
    for m in range(months + 1):
        data.append((current_date.strftime('%Y-%m-%d'), current_value))
        current_date += pd.DateOffset(months=1)
        current_value *= (1 + appreciation / 12)
    
    df = pd.DataFrame(data, columns=["Date", "Forecasted HEI Value"])
    df.index.name = "Month"
    return df

st.title("HEI Forecast Calculator")

# Inputs
home_value = st.number_input("Home Value ($)", value=1000000.0, step=1000.0)
appreciation = st.number_input("Appreciation Rate (Annual, as decimal)", value=0.03, step=0.01)
origination_date = st.date_input("Origination Date", value=datetime.date(2023, 12, 11))

if st.button("Generate 120-Month Forecast"):
    forecast_df = calculate_forecast(home_value, appreciation, origination_date, months=120)
    st.write("### 120-Month HEI Forecast")
    st.dataframe(forecast_df.style.format({"Forecasted HEI Value": "$ {:,.2f}"}))
