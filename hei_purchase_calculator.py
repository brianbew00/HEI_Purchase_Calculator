import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Function to calculate values
def calculate_hei(home_value, appreciation_rate, premium_percentage, hei_multiplier, investor_cap):
    years = np.arange(0, 11)
    home_values = [home_value * ((1 + appreciation_rate)**year) for year in years]
    premium_amount = home_value * premium_percentage
    investor_percentage = premium_percentage * hei_multiplier
    hei_caps = [premium_amount * ((1 + investor_cap)**year) for year in years]
    hei_intrinsic_values = [hv * investor_percentage for hv in home_values]
    settlement_values = [min(cap, intrinsic) for cap, intrinsic in zip(hei_caps, hei_intrinsic_values)]

    df = pd.DataFrame({
        "Year": years,
        "Home Value": home_values,
        "HEI Cap": hei_caps,
        "HEI Intrinsic Value": hei_intrinsic_values,
        "Settlement Value": settlement_values
    })

    return premium_amount, investor_percentage, df

# Streamlit Page Configuration
st.set_page_config(page_title="HEI Calculator", layout="wide")

# Title
st.title("🏠 Home Equity Investment (HEI) Calculator")

# Sidebar Inputs
with st.sidebar:
    st.header("🔧 Calculator Inputs")

    home_value = st.number_input("Home Value", value=1_000_000, step=10_000, format="$%d")
    appreciation_rate = st.number_input("Appreciation Rate (%)", value=2.0, step=0.1, format="%.2f%%") / 100
    premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=1.0, format="%.2f%%") / 100
    hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1, format="%.1fx")
    investor_cap = st.number_input("Investor Cap (%)", value=20.0, step=1.0, format="%.2f%%") / 100

# Calculations
premium_amount, investor_percentage, df_results = calculate_hei(
    home_value, appreciation_rate, premium_percentage, hei_multiplier, investor_cap
)

# Display Calculated Premium and Investor Percentages
col1, col2 = st.columns(2)

with col1:
    st.metric("Premium Amount", f"${premium_amount:,.0f}")

with col2:
    st.metric("Investor Percentage", f"{investor_percentage:.0%}")

# Plotly Chart (Similar to Chart.js from HTML)
fig = go.Figure()

fig.add_trace(go.Scatter(x=df_results["Year"], y=df_results["Home Value"], mode='lines+markers', name="Home Value"))
fig.add_trace(go.Scatter(x=df_results["Year"], y=df_results["HEI Cap"], mode='lines+markers', name="HEI Cap"))
fig.add_trace(go.Scatter(x=df_results["Year"], y=df_results["HEI Intrinsic Value"], mode='lines+markers', name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=df_results["Year"], y=df_results["Settlement Value"], mode='lines+markers', name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title="HEI Value Over Time",
    xaxis_title="Year",
    yaxis_title="Value ($)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Display Results Table
st.subheader("📊 Detailed Annual Breakdown")
st.dataframe(
    df_results.style.format({
        "Home Value": "${:,.0f}",
        "HEI Cap": "${:,.0f}",
        "HEI Intrinsic Value": "${:,.0f}",
        "Settlement Value": "${:,.0f}"
    }),
    use_container_width=True,
    hide_index=True
)
