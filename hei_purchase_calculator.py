import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏡 Home Equity Investment (HEI) Calculator")

# Sanity Check: Ensure latest version is loaded
st.success("✅ The latest version of the app has been loaded.")

# Sidebar Inputs
with st.sidebar:
    st.header("🛠️ Input Parameters")
    
    home_value = st.number_input(
        "Home Value ($)", min_value=0, value=1_000_000, step=10_000, format="%d"
    )

    appreciation_rate = st.number_input(
        "Annual Appreciation Rate (%)", value=2.0, step=0.1, format="%.2f"
    ) / 100

    premium_percentage = st.number_input(
        "Premium Percentage (%)", value=20.0, step=0.1, format="%.2f"
    ) / 100

    hei_multiplier = st.number_input(
        "HEI Multiplier", value=2.0, step=0.1, format="%.2f"
    )

    investor_cap_rate = st.number_input(
        "Investor Cap (%)", value=20.0, step=0.1, format="%.2f"
    ) / 100

# Initial calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

# Lists for storing calculation results
years = list(range(11))
home_values = []
hei_caps = []
hei_intrinsic_values = []
settlement_values = []

# Set initial values
current_home_value = home_value
hei_cap = premium_amount

# Calculate values for each year
for year in years:
    if year > 0:
        current_home_value *= (1 + appreciation_rate)
        hei_cap *= (1 + investor_cap_rate)

    hei_intrinsic_value = current_home_value * investor_percentage
    settlement_value = min(hei_cap, hei_intrinsic_value)

    home_values.append(current_home_value)
    hei_caps.append(hei_cap)
    hei_intrinsic_values.append(hei_intrinsic_value)
    settlement_values.append(settlement_value)

# Create DataFrame
df_results = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values,
})

# Format the DataFrame for display
df_display = df_results.copy()
currency_format = lambda x: "${:,.0f}".format(x)

df_display["Home Value"] = df_display["Home Value"].map(currency_format)
df_display["HEI Cap"] = df_display["HEI Cap"].map(currency_format)
df_display["HEI Intrinsic Value"] = df_display["HEI Intrinsic Value"].map(currency_format)
df_display["Settlement Value"] = df_display["Settlement Value"].map(currency_format)

# Display premium and investor percentage neatly
col1, col2 = st.columns(2)

with col1:
    st.metric("🏷️ Premium Amount", currency_format(premium_amount))
with col2:
    st.metric("Investor Percentage", f"{investor_percentage:.0%}")

# Plotly interactive chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=years, y=home_values, name="Home Value", mode='lines+markers'))
fig.add_trace(go.Scatter(
    x=years, y=hei_caps, name="HEI Cap", line=dict(dash='dash')))
fig.add_trace(go.Scatter(
    x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value"
))
fig.add_trace(go.Scatter(
    x=years, y=settlement_values, name="Settlement Value",
    fill='tozeroy'
))

fig.update_layout(
    title="HEI Investment Values Over 10 Years",
    xaxis_title="Year",
    yaxis_title="Value ($)",
    hovermode="x unified",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Display detailed results
st.subheader("📊 Annual HEI Breakdown")
st.dataframe(df_display.set_index("Year"), use_container_width=True)
