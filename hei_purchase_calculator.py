import streamlit as st
import pandas as pd
import datetime

def calculate_forecast(home_value, appreciation, origination_date, months=120):
    """
    Forecast the home's value month-by-month using the formula:
    
      Forecasted HEI Value = home_value * (1 + appreciation)^(month / 12)
    
    where appreciation is already in decimal form.
    
    Returns a DataFrame with:
      - Index labeled as "Month"
      - Columns: Date, Forecasted HEI Value
    """
    data = []
    for m in range(months + 1):
        forecasted_value = home_value * ((1 + appreciation) ** (m / 12))
        forecast_date = pd.to_datetime(origination_date) + pd.DateOffset(months=m)
        data.append((forecast_date.strftime('%Y-%m-%d'), forecasted_value))
    
    df = pd.DataFrame(data, columns=["Date", "Forecasted HEI Value"])
    df.index.name = "Month"
    return df

st.title("HEI Forecast Calculator")

# Primary inputs
home_value = st.number_input("Home Value ($)", value=1000000.0, step=1000.0)
# Appreciation entered as a whole number percentage (e.g., 3 for 3%)
appreciation_input = st.number_input("Appreciation Rate (Annual %)", value=3.0, step=0.1)
# Convert the percentage to a decimal
appreciation = appreciation_input / 100.0
origination_date = st.date_input("Origination Date", value=datetime.date(2023, 12, 11))

# Inputs for Option Value calculation
original_hei_amount = st.number_input("Original HEI Amount ($)", value=200000.0, step=1000.0)
multiplier = st.number_input("Multiplier", value=2.0, step=0.1)

# Investor Cap input (entered as a whole number percentage, default is 20%)
investor_cap_input = st.number_input("Investor Cap (%)", value=20.0, step=0.1)
# Convert to decimal form
investor_cap = investor_cap_input / 100.0

if st.button("Generate 120-Month Forecast"):
    # Generate the forecast table out to 120 months.
    forecast_df = calculate_forecast(home_value, appreciation, origination_date, months=120)
    
    # Calculate Option Value for each month:
    #   Option Value = Forecasted HEI Value * ((Original HEI Amount / Home Value) * Multiplier)
    option_value_multiplier = (original_hei_amount / home_value) * multiplier
    forecast_df["Option Value"] = forecast_df["Forecasted HEI Value"] * option_value_multiplier
    
    # Calculate the cap amount based on Investor Cap and Original HEI Amount.
    cap_amount = investor_cap * original_hei_amount
    
    # For each month, apply the cap to the Option Value.
    forecast_df["Capped Option Value"] = forecast_df["Option Value"].apply(lambda x: min(x, cap_amount))
    
    # Display the forecast table with the new column.
    st.write("### 120-Month HEI Forecast")
    st.dataframe(forecast_df.style.format({
        "Forecasted HEI Value": "$ {:,.2f}",
        "Option Value": "$ {:,.2f}",
        "Capped Option Value": "$ {:,.2f}"
    }))
