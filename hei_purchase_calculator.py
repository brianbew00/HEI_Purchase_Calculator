import streamlit as st
import pandas as pd
import datetime

def calculate_forecast(home_value, appreciation, origination_date, months):
    """
    Forecast the home’s value month-by-month using monthly compounding.
    Returns a DataFrame with the forecast for each month.
    """
    data = []
    current_value = home_value
    current_date = pd.to_datetime(origination_date)
    
    # Include month 0 (the origination date) up through the specified number of months.
    for m in range(months + 1):
        data.append((m, current_date.strftime('%Y-%m-%d'), current_value))
        current_date += pd.DateOffset(months=1)
        current_value *= (1 + appreciation / 12)
    df = pd.DataFrame(data, columns=["Month", "Date", "Forecasted HEI Value"])
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

# --- Input widgets ---
home_value = st.number_input("Home Value ($)", value=200000.0, step=1000.0)
original_amount = st.number_input("Original HEI Amount ($)", value=200000.0, step=1000.0)
multiplier = st.number_input("Multiplier", value=2.0, step=0.1)
origination_date = st.date_input("Origination Date", value=datetime.date(2023, 12, 11))
purchase_date = st.date_input("Purchase Date", value=datetime.date(2024, 2, 24))
st.info("Enter Premium / Discount as a decimal (e.g. 0.06 for a 6% premium, -0.06 for a 6% discount).")
premium_discount = st.number_input("Premium / Discount", value=0.06, step=0.01)
st.info("Investor Cap represents the maximum profit as a fraction of the original HEI amount (e.g., 0.2 means 20%).")
investor_cap = st.number_input("Investor Cap", value=0.2, step=0.01)
appreciation = st.number_input("Appreciation Rate (Annual, as a decimal)", value=0.03, step=0.01)

if st.button("Calculate"):
    # 1. Option Value
    option_value = (original_amount / home_value) * multiplier

    # 2. Contract Age (in full months)
    contract_age = full_months_between(origination_date, purchase_date)
    
    # 3. Forecast HEI value at the purchase date (i.e. at contract_age)
    forecast_df = calculate_forecast(home_value, appreciation, origination_date, contract_age)
    forecasted_value_at_purchase = forecast_df.loc[forecast_df['Month'] == contract_age, 'Forecasted HEI Value'].values[0]
    
    # 4. Purchase Price: apply premium/discount to the forecasted value
    purchase_price = forecasted_value_at_purchase * (1 + premium_discount)
    
    # 5. Compute the investor’s gross return and then apply the cap.
    gross_return = purchase_price * option_value
    profit = gross_return - original_amount
    if profit > 0:
        capped_profit = min(profit, investor_cap * original_amount)
    else:
        capped_profit = profit
    sale_price = original_amount + capped_profit

    # Prepare a detailed results dictionary.
    results = {
        "Option Value": round(option_value, 4),
        "Contract Age (Months)": contract_age,
        "Forecasted HEI Value at Purchase": round(forecasted_value_at_purchase, 2),
        "Purchase Price": round(purchase_price, 0),
        "Gross Return": round(gross_return, 0),
        "Profit": round(profit, 0),
        "Capped Profit": round(capped_profit, 0),
        "Final Investor Value (Sale Price)": round(sale_price, 0)
    }
    
    # If you want to output only the three values you mentioned, you could do:
    # simple_results = {
    #     "Contract Age (Months)": contract_age,
    #     "Purchase Price": round(purchase_price, 0),
    #     "Sale Price": round(sale_price, 0)
    # }
    # st.json(simple_results)
    
    st.write("### Detailed Results")
    st.json(results)
    
    st.write("### Forecasted HEI Value Over Time")
    st.dataframe(forecast_df.style.format({"Forecasted HEI Value": "$ {:,.2f}"}))
