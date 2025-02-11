import streamlit as st
import pandas as pd
import datetime

def calculate_forecast(home_value, appreciation, origination_date, months=120):
    """
    Forecast the home's value month-by-month using the formula:
      Forecasted HEI Value = home_value * (1 + appreciation)^(month / 12)
    where appreciation is in decimal form.
    
    Returns a DataFrame with:
      - The index labeled as "Month"
      - Columns: Date, Forecasted HEI Value
    """
    data = []
    for m in range(months + 1):
        forecasted_value = home_value * ((1 + appreciation) ** (m / 12))
        forecast_date = pd.to_datetime(origination_date) + pd.DateOffset(months=m)
        # Format the date as MM/DD/YYYY
        formatted_date = forecast_date.strftime('%m/%d/%Y')
        data.append((formatted_date, forecasted_value))
    
    df = pd.DataFrame(data, columns=["Date", "Forecasted HEI Value"])
    df.index.name = "Month"
    return df

st.title("HEI Forecast Calculator")

# Primary inputs
home_value = st.number_input("Home Value ($)", value=1000000.0, step=1000.0)

# Appreciation entered as a whole number percentage (e.g., 3 for 3%)
appreciation_input = st.number_input("Appreciation Rate (Annual %)", value=3.0, step=0.1)
# Convert to decimal
appreciation = appreciation_input / 100.0

origination_date = st.date_input("Origination Date", value=datetime.date(2023, 12, 11))

# Inputs for Option Value calculation
original_hei_amount = st.number_input("Original HEI Amount ($)", value=200000.0, step=1000.0)
multiplier = st.number_input("Multiplier", value=2.0, step=0.1)

# Investor Cap input (entered as a whole number percentage, default is 20%)
investor_cap_input = st.number_input("Investor Cap (%)", value=20.0, step=0.1)
# Convert to decimal
investor_cap = investor_cap_input / 100.0

if st.button("Generate 120-Month Forecast"):
    # Generate the forecast table out to 120 months.
    forecast_df = calculate_forecast(home_value, appreciation, origination_date, months=120)
    
    # Calculate Option Value for each month:
    #   Option Value = Forecasted HEI Value * ((Original HEI Amount / Home Value) * Multiplier)
    option_value_multiplier = (original_hei_amount / home_value) * multiplier
    forecast_df["Option Value"] = forecast_df["Forecasted HEI Value"] * option_value_multiplier
    
    # Calculate the Investor Cap Value for each month using:
    #   Investor Cap Value = Original HEI Amount * (1 + investor_cap)^(month / 12)
    forecast_df["Investor Cap Value"] = original_hei_amount * ((1 + investor_cap) ** (forecast_df.index / 12))
    
    # Rename columns to match desired labels:
    # "Forecasted HEI Value" becomes "Home Value"
    # "Option Value" becomes "Contract Value"
    # "Investor Cap Value" becomes "Investor Cap"
    forecast_df.rename(columns={
        "Forecasted HEI Value": "Home Value",
        "Option Value": "Contract Value",
        "Investor Cap Value": "Investor Cap"
    }, inplace=True)
    
    # Add the Acquisition Premium column.
    # Acquisition Premium = max(1 - (Investor Cap / Contract Value), 0)
    forecast_df["Acquisition Premium"] = forecast_df.apply(
        lambda row: max(1 - (row["Investor Cap"] / row["Contract Value"]), 0),
        axis=1
    )
    
    # Add the Settlement Value column.
    # Settlement Value = minimum of Contract Value and Investor Cap.
    forecast_df["Settlement Value"] = forecast_df.apply(
        lambda row: min(row["Contract Value"], row["Investor Cap"]),
        axis=1
    )
    
    # Reorder the columns for display: Month (index), Date, Home Value, Contract Value, Investor Cap, Acquisition Premium, Settlement Value
    forecast_df = forecast_df[["Date", "Home Value", "Contract Value", "Investor Cap", "Acquisition Premium", "Settlement Value"]]
    
    st.write("### 120-Month HEI Forecast")
    st.dataframe(
        forecast_df.style.format({
            "Home Value": "$ {:,.2f}",
            "Contract Value": "$ {:,.2f}",
            "Investor Cap": "$ {:,.2f}",
            "Acquisition Premium": "{:.2%}",
            "Settlement Value": "$ {:,.2f}"
        })
    )
