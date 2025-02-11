import streamlit as st
import pandas as pd
import datetime

def calculate_hei(home_value, appreciation, origination_date, months=121):
    """
    Forecast the home’s value over a number of months using monthly compounding.
    """
    data = []
    current_date = origination_date
    current_value = home_value
    
    for month in range(months):
        data.append([current_date.strftime('%Y-%m-%d'), month, round(current_value, 2)])
        current_date += pd.DateOffset(months=1)
        current_value *= (1 + appreciation / 12)
    
    df = pd.DataFrame(data, columns=["Date", "Month", "Home Value"])
    return df

def full_months_between(start_date, end_date):
    """
    Calculate the number of full months between two dates.
    """
    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    if end_date.day < start_date.day:
        months -= 1
    return months

st.title("Home Equity Investment Simulator")

# User inputs
home_value = st.number_input("Home Value ($)", value=1000000.0, step=1000.0)
original_amount = st.number_input("Original HEI Amount ($)", value=200000.0, step=1000.0)
multiplier = st.number_input("Multiplier", value=2.0, step=0.1)
# (We will calculate option value from these inputs.)
origination_date = st.date_input("Origination Date", value=datetime.date(2023, 12, 11))
purchase_date = st.date_input("Purchase Date", value=datetime.date(2024, 2, 24))
st.info("Premium / Discount should be entered as a decimal. For example, 0.06 represents a 6% premium, while -0.06 would represent a 6% discount.")
premium_discount = st.number_input("Premium / Discount", value=0.06, step=0.01)
st.info("Investor Cap is the maximum profit (as a fraction of the original HEI amount) the investor can earn. For example, 0.2 represents a 20% cap.")
investor_cap = st.number_input("Investor Cap", value=0.2, step=0.01)
appreciation = st.number_input("Appreciation Rate (Annual)", value=0.03, step=0.01)

if st.button("Calculate"):
    # 1. Calculate Option Value:
    #    option_value = (original_amount / home_value) * multiplier
    option_value = (original_amount / home_value) * multiplier
    
    # 2. Calculate Contract Age (number of full months between origination and purchase)
    contract_age = full_months_between(origination_date, purchase_date)
    
    # 3. Forecast the HEI (home value) over 120 months starting from origination_date.
    forecast_df = calculate_hei(home_value, appreciation, pd.to_datetime(origination_date))
    
    # 4. Retrieve the forecasted home value at the contract age.
    if contract_age < len(forecast_df):
        forecasted_value_at_purchase = forecast_df.loc[forecast_df['Month'] == contract_age, 'Home Value'].values[0]
    else:
        st.error("Contract age is beyond the forecast range. Using the final available forecast value.")
        forecasted_value_at_purchase = forecast_df['Home Value'].iloc[-1]
    
    # 5. Calculate Purchase Pricing:
    #    Here we adjust the forecasted HEI by (1 + premium_discount)
    purchase_pricing = forecasted_value_at_purchase * (1 + premium_discount)
    
    # 6. Compute the Investor’s Gross Return based on the option value and purchase pricing.
    gross_return = purchase_pricing * option_value
    profit = gross_return - original_amount
    
    # Apply the investor cap to the profit (only if the profit is positive)
    if profit > 0:
        capped_profit = min(profit, investor_cap * original_amount)
    else:
        capped_profit = profit
    
    final_investor_value = original_amount + capped_profit
    
    # Display the results
    st.write("### Simulation Results")
    st.write(f"**Option Value:** {option_value:.4f}")
    st.write(f"**Contract Age (months):** {contract_age}")
    st.write(f"**Forecasted HEI Value at Purchase Date:** ${forecasted_value_at_purchase:,.2f}")
    st.write(f"**Purchase Pricing:** ${purchase_pricing:,.2f}")
    st.write(f"**Gross Return:** ${gross_return:,.2f}")
    st.write(f"**Profit (after applying cap if applicable):** ${capped_profit:,.2f}")
    st.write(f"**Final Investor Value:** ${final_investor_value:,.2f}")
    
    st.write("### 120-Month Home Value Forecast")
    st.dataframe(forecast_df.style.format({"Home Value": "$ {:,.2f}"}))
