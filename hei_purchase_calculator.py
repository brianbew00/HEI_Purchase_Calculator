import streamlit as st
import pandas as pd

st.title("Home Equity Investment (HEI) Calculator")

# User inputs (using number_input for numeric values)
home_value = st.number_input("Home Value ($)", value=1000000, step=10000)
home_price_appreciation = st.number_input("Appreciation (%)", value=2.0, step=0.1) / 100
premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=0.1) / 100
hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1)
investor_cap = st.number_input("Investor Cap (%)", value=20.0, step=0.1) / 100

# Derived calculations
premium_amount = home_value * premium_percentage
investor_percentage = hei_multiplier * premium_percentage

st.write("**Premium Amount:**", f"${premium_amount:,.0f}")
st.write("**Investor Percentage:**", f"{investor_percentage*100:.0f}%")

# Initialize lists for yearly values
years = []
home_values = []
hei_caps = []
hei_intrinsic_values = []
settlement_values = []

# Year 0 calculations
years.append(0)
home_values.append(home_value)
current_hei_cap = premium_amount
hei_caps.append(current_hei_cap)
hei_intrinsic = investor_percentage * home_value
hei_intrinsic_values.append(hei_intrinsic)
settlement_values.append(min(current_hei_cap, hei_intrinsic))

# Calculate values for years 1 to 10
current_home_value = home_value
for year in range(1, 11):
    current_hei_cap *= (1 + investor_cap)
    current_home_value *= (1 + home_price_appreciation)
    hei_intrinsic = investor_percentage * current_home_value
    settlement = min(current_hei_cap, hei_intrinsic)
    
    years.append(year)
    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    hei_intrinsic_values.append(hei_intrinsic)
    settlement_values.append(settlement)

# Create a DataFrame to display the results
df = pd.DataFrame({
    "Year": years,
    "Home Value": [round(val) for val in home_values],
    "HEI Cap": [round(val) for val in hei_caps],
    "HEI Intrinsic Value": [round(val) for val in hei_intrinsic_values],
    "Settlement Value": [round(val) for val in settlement_values],
})
st.subheader("Calculation Results")
st.table(df)

# Plot the results as a line chart
chart_data = df.set_index("Year")
st.subheader("HEI Calculator Chart")
st.line_chart(chart_data)
