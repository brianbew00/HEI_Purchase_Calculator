import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="HEI Calculator", layout="wide")

# Main title
st.title("🏠 Home Equity Investment (HEI) Calculator")

# Sidebar Inputs
with st.sidebar:
    st.header("🛠️ Inputs")
    home_value = st.number_input("Home Value", value=1_000_000, step=10_000, format="%d")
    appreciation_rate = st.number_input("Appreciation (%)", value=2.0, step=0.1, format="%.2f") / 100
    premium_percentage = st.number_input("Premium Percentage", value=20.0, step=0.1, format="%.2f") / 100
    hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1)
    investor_cap_rate = st.number_input("Investor Cap (%)", value=20.0, step=0.1) / 100

# Calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

# Data preparation
years = list(range(11))
home_values = [home_value]
hei_caps = [premium_amount]
hei_intrinsic_values = [home_value * investor_percentage]
settlement_values = [min(hei_caps[0], hei_intrinsic_values[0])]

for year in range(1, 11):
    new_home_value = home_values[-1] * (1 + appreciation_rate)
    new_hei_cap = hei_caps[-1] * (1 + investor_cap_rate)
    new_intrinsic_value = new_home_value * investor_percentage
    settlement_value = min(new_hei_cap, new_intrinsic_value)

    home_values.append(new_home_value)
    hei_caps.append(new_hei_cap)
    hei_intrinsic_values.append(new_intrinsic_value)
    settlement_values.append(settlement_value)

# Results DataFrame
results_df = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values
})

# Display calculated Premium Amount and Investor Percentage neatly
col1, col2 = st.columns(2)
col1.metric("🏷️ Premium Amount", f"${premium_amount:,.0f}")
col2.metric("Investor Percentage", f"{investor_percentage:.0%}")

# Plotly Interactive Chart (similar to original Chart.js visualization)
fig = go.Figure()

fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value", line=dict(width=2)))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap", line=dict(width=2)))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value", line=dict(width=2)))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy', line=dict(width=2)))

fig.update_layout(
    title="HEI Analysis Over 10 Years",
    xaxis_title="Year",
    yaxis_title="Value ($)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Display Formatted Table
st.subheader("📊 Annual HEI Breakdown")

def format_currency(x):
    return "${:,.0f}".format(x)

formatted_df = results_df.copy()
formatted_df["Home Value"] = formatted_df["Home Value"].apply(format_currency)
formatted_df["HEI Cap"] = formatted_df["HEI Cap"].apply(format_currency)
formatted_df["HEI Intrinsic Value"] = formatted_df["HEI Intrinsic Value"].apply(format_currency)
formatted_df["Settlement Value"] = formatted_df["Settlement Value"].apply(format_currency)

st.dataframe(formatted_df.set_index("Year"), use_container_width=True)

