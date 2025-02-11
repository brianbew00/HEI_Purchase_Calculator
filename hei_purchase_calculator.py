import streamlit as st
import pandas as pd
import datetime

def calculate_forecast(home_value, appreciation, origination_date, months=120):
    """
    Forecast the home's value month-by-month using the formula:
    
    forecasted_value = home_value * (1 + appreciation)^(month / 12)
    
    Returns a DataFrame with:
      - Index labeled as "Month"
      - Columns: Date, Forecasted HEI Value
    """
    data = []
    for m in range(months + 1):
        # Calculate the forecasted HEI value at month m
        forecasted_value = home_value * ((1 + appreciation) ** (m / 12))
        # Calculate the corresponding date by adding m months to the origination date
        forecast_date = pd.to_datetime(origination_date) + pd.DateOffset(months=m)
        data.append((forecast_date.strftime('%Y-%m-%d'), forecasted_value))
    
    df = pd.DataFrame(data, columns=["Date", "Forecasted HEI Value"])
    df.index.name = "Month"
    return df

st.title("HEI Forecast Calculator")

# Primary inputs
home_value = st.number_input("Home Value ($)", value=1000000.0, step=1000.0)
appreciation = st.number_input("Appreciation Rate (Annual, as decimal)", value=0.03, step=0.01)
origination_date = st.date_input("Origination Date", value=datetime.date(2023, 12, 11))

# New inputs for the Option Value calculation
original_hei_amount = st.number_input("Original HEI Amount ($)", value=200000.0, step=1000.0)
multiplier = st.number_input("Multiplier", value=2.0, step=0.1)

if st.button("Generate 120-Month Forecast"):
    # Generate the forecast table for 120 months
    forecast_df = calculate_forecast(home_value, appreciation, origination_date, months=120)
    
    # Compute the option value multiplier from the user inputs.
    # This multiplier is constant for all rows.
    option_value_multiplier = (original_hei_amount / home_value) * multiplier
    
    # Compute the Option Value for each row (month)
    forecast_df["Option Value"] = forecast_df["Forecasted HEI Value"] * option_value_multiplier
    
    # Display the forecast table with both columns. The DataFrame's index is labeled "Month".
    st.write("### 120-Month HEI Forecast")
    st.dataframe(
        forecast_df.style.format({
            "Forecasted HEI Value": "$ {:,.2f}",
            "Option Value": "$ {:,.2f}"
        })
    )
