import streamlit as st
import pandas as pd
import datetime

def calculate_forecast(home_value, appreciation, origination_date, months=120):
    """
    Forecast the home’s value month-by-month using the formula:
    forecasted_value = home_value * (1 + appreciation)^(month/12)
    
    Returns a DataFrame with the index labeled as "Month", and columns for Date and Forecasted HEI Value.
    """
    data = []
    for m in range(months + 1):
        # Calculate the forecasted value for month 'm'
        forecasted_value = home_value * ((1 + appreciation) ** (m / 12))
        # Calculate the corresponding date by adding 'm' months to the origination date
        forecast_date = pd.to_datetime(origination_date) + pd.DateOffset(months=m)
        data.append((forecast_date.strftime('%Y-%m-%d'), forecasted_value))
        
    # Create the DataFrame without an explicit "Month" column; use the index as Month
    df = pd.DataFrame(data, columns=["Date", "Forecasted HEI Value"])
    df.index.name = "Month"
    return df

st.title("HEI Forecast Calculator")

# Input widgets
home_value = st.number_input("Home Value ($)", value=1000000.0, step=1000.0)
appreciation = st.number_input("Appreciation Rate (Annual, as decimal)", value=0.03, step=0.01)
origination_date = st.date_input("Origination Date", value=datetime.date(2023, 12, 11))

if st.button("Generate 120-Month Forecast"):
    forecast_df = calculate_forecast(home_value, appreciation, origination_date, months=120)
    st.write("### 120-Month HEI Forecast")
    st.dataframe(forecast_df.style.format({"Forecasted HEI Value": "$ {:,.2f}"}))
