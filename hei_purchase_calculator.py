import streamlit as st
import pandas as pd
import numpy as np
import datetime

def calculate_forecast(home_value, appreciation, origination_date, months=120):
    """
    Forecast the home's value month-by-month using the formula:
      Home Value = home_value * (1 + appreciation)^(month / 12)
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

with st.form(key="forecast_form"):
    st.subheader("Primary Inputs")
    col1, col2, col3 = st.columns(3)
    with col1:
        home_value = st.number_input("Home Value ($)", value=1000000.0, step=1000.0)
    with col2:
        appreciation_input = st.number_input("Appreciation Rate (Annual %)", value=3.0, step=0.1)
    with col3:
        origination_date = st.date_input("Origination Date", value=datetime.date(2023, 12, 11))
    # Convert appreciation from whole number to decimal.
    appreciation = appreciation_input / 100.0

    st.subheader("Option & Investor Inputs")
    col1, col2, col3 = st.columns(3)
    with col1:
        original_hei_amount = st.number_input("Original HEI Amount ($)", value=200000.0, step=1000.0)
    with col2:
        multiplier = st.number_input("Multiplier", value=2.0, step=0.1)
    with col3:
        investor_cap_input = st.number_input("Investor Cap (%)", value=20.0, step=0.1)
    investor_cap = investor_cap_input / 100.0
    col1, col2 = st.columns(2)
    with col1:
        premium_discount_input = st.number_input("Premium / Discount (%)", value=6.0, step=0.1)
    with col2:
        st.write("")  # empty column for spacing
    premium_discount = premium_discount_input / 100.0

    st.subheader("Secondary Market Investment (Acquisition) Inputs")
    sec_method = st.radio("Determine secondary market investment by:", 
                          options=["Contract Age (months)", "Purchase Date"])
    if sec_method == "Contract Age (months)":
        sec_contract_age = st.number_input("Contract Age (months)", value=12, step=1)
        sec_purchase_date = None
    else:
        sec_purchase_date = st.date_input("Secondary Purchase Date", value=datetime.date(2024, 12, 11))
        sec_contract_age = None
        
    submitted = st.form_submit_button(label="Generate 120-Month Forecast")

if submitted:
    # Generate the 120-month forecast.
    forecast_df = calculate_forecast(home_value, appreciation, origination_date, months=120)
    
    # Calculate Contract Value:
    #   Contract Value = Forecasted HEI Value * ((Original HEI Amount / Home Value) * Multiplier)
    option_value_multiplier = (original_hei_amount / home_value) * multiplier
    forecast_df["Option Value"] = forecast_df["Forecasted HEI Value"] * option_value_multiplier
    
    # Calculate Investor Cap:
    #   Investor Cap = Original HEI Amount * (1 + investor_cap)^(month / 12)
    forecast_df["Investor Cap Value"] = original_hei_amount * ((1 + investor_cap) ** (forecast_df.index / 12))
    
    # Rename columns:
    # "Forecasted HEI Value" → "Home Value"
    # "Option Value" → "Contract Value"
    # "Investor Cap Value" → "Investor Cap"
    forecast_df.rename(columns={
        "Forecasted HEI Value": "Home Value",
        "Option Value": "Contract Value",
        "Investor Cap Value": "Investor Cap"
    }, inplace=True)
    
    # Add Acquisition Premium:
    # Acquisition Premium = max(1 - (Investor Cap / Contract Value), 0)
    forecast_df["Acquisition Premium"] = forecast_df.apply(
        lambda row: max(1 - (row["Investor Cap"] / row["Contract Value"]), 0),
        axis=1
    )
    
    # Add Settlement Value:
    # Settlement Value = min(Contract Value, Investor Cap)
    forecast_df["Settlement Value"] = np.minimum(forecast_df["Contract Value"], forecast_df["Investor Cap"])
    
    # Add Secondary Market Value - Acquisition:
    # = Settlement Value * (1 + Premium/Discount)
    forecast_df["Secondary Market Value - Acquisition"] = forecast_df["Settlement Value"] * (1 + premium_discount)
    
    # Add the new column: Secondary Market Investment (Acquisition)
    # Set it to blank (empty string) for all rows, then fill in the target row.
    forecast_df["Secondary Market Investment (Acquisition)"] = ""
    
    # Determine the target month:
    if sec_method == "Contract Age (months)":
        target_month = int(sec_contract_age)
    else:
        # Convert the forecast dates (strings) back to datetime.
        forecast_dates = pd.to_datetime(forecast_df["Date"], format="%m/%d/%Y")
        # Find the first index where forecast date >= secondary purchase date.
        target_month = forecast_dates[forecast_dates >= pd.to_datetime(sec_purchase_date)].index.min()
        if pd.isna(target_month):
            target_month = forecast_df.index[-1]
    
    # In the target month row, set the new column value to the Secondary Market Value - Acquisition.
    forecast_df.loc[target_month, "Secondary Market Investment (Acquisition)"] = forecast_df.loc[target_month, "Secondary Market Value - Acquisition"]
    
    # Reorder columns for display:
    final_cols = [
        "Date", 
        "Home Value", 
        "Contract Value", 
        "Investor Cap", 
        "Acquisition Premium", 
        "Settlement Value", 
        "Secondary Market Value - Acquisition", 
        "Secondary Market Investment (Acquisition)"
    ]
    forecast_df = forecast_df[final_cols]
    
    st.write("### 120-Month HEI Forecast")
    st.dataframe(
        forecast_df.style.format({
            "Home Value": "$ {:,.2f}",
            "Contract Value": "$ {:,.2f}",
            "Investor Cap": "$ {:,.2f}",
            "Acquisition Premium": "{:.2%}",
            "Settlement Value": "$ {:,.2f}",
            "Secondary Market Value - Acquisition": "$ {:,.2f}",
            "Secondary Market Investment (Acquisition)": "$ {:,.2f}"
        })
    )
