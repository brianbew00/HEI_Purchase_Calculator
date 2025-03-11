import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏡 Home Equity Investment (HEI) Calculator")

# Sidebar Inputs
with st.sidebar:
    st.header("🛠️ Input Parameters")

    home_value = st.number_input("Home Value", value=1_000_000, step=10_000, format="%d")
    appreciation_rate = st.number_input("Annual Appreciation Rate (%)", value=2.0, step=0.1) / 100
    premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=0.1, format="%.1f") / 100
    hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1)
    investor_cap_rate = st.number_input("Investor Cap (%)", value=20.0, step=0.1) / 100

# Perform Calculations
years = list(range(11))
home_values = []
hei_caps = []
hei_intrinsic_values = []
settlement_values = []

premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

current_home_value = home_value
hei_cap = premium_amount

for year in years:
    if year > 0:
        home_value *= (1 + appreciation_rate)
        hei_cap *= (1 + investor_cap_rate)

    hei_intrinsic_value = home_value * investor_percentage
    settlement_value = min(hei_cap, hei_intrinsic_value)

    years[year] = year
    home_values.append(home_value)
    hei_caps.append(hei_cap)
    hei_intrinsic_values.append(hei_intrinsic_value)
    settlement_values.append(settlement_value)

# Prepare DataFrame
df_results = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values
})

# Formatted metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Premium Amount", f"${home_values[0] * premium_percentage:,.0f}")
with col2:
    st.metric("Investor Percentage", f"{investor_percentage:.0%}")

# Plotly Chart
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value"))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap"))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill="tozeroy"))

fig.update_layout(
    title="HEI Investment Growth",
    xaxis_title="Year",
    yaxis_title="Value ($)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Table with proper formatting
st.subheader("📊 Detailed Results")

df_display = df_results.copy()
df_display["Home Value"] = df_display["Home Value"].apply(lambda x: f"${x:,.0f}")
df_display["HEI Cap"] = df_display["HEI Cap"].apply(lambda x: f"${x:,.0f}")
df_display["HEI Intrinsic Value"] = df_display["HEI Intrinsic Value"].apply(lambda x: f"${x:,.0f}")
df_display["Settlement Value"] = df_display["Settlement Value"].apply(lambda x: f"${x:,.0f}")

st.dataframe(df_display.set_index("Year"), use_container_width=True)

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value"))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap"))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title="HEI Investment Values Over 10 Years",
    xaxis_title="Year",
    yaxis_title="Value ($)",
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)
