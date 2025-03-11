import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Streamlit page setup
st.set_page_config(page_title="HEI Calculator", layout="wide")

st.title("🏠 Home Equity Investment (HEI) Calculator")

# Sidebar input fields
with st.sidebar:
    st.header("🔧 Inputs")
    home_value = st.number_input("Home Value ($)", value=1000000, step=10000)
    appreciation = st.number_input("Appreciation Rate (%)", value=2.0, step=0.1) / 100
    premium_pct = st.number_input("Premium Percentage (%)", value=20.0, step=0.1) / 100
    hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1)
    investor_cap = st.number_input("Investor Cap (%)", value=20.0, step=0.1) / 100

# Calculations
premium_amount = home_value = home_value = 1_000_000 * premium_pct
investor_pct = premium_pct * hei_multiplier
hei_cap = premium_amount

# Calculation for 10 years
years = np.arange(0, 11)
home_values = [home_value := 1_000_000]
hei_caps = [hei_cap]
hei_intrinsic_values = [investor_percentage := investor_pct * home_value]
settlement_values = [min(hei_cap, hei_intrinsic_values[0])]

for year in years[1:]:
    home_value *= (1 + appreciation)
    hei_cap *= (1 + investor_cap := 0.20)  # Assuming investorCap from your original code as 20%
    hei_intrinsic_value = investor_percentage * home_value
    settlement_value = min(hei_cap, hei_intrinsic_value)

    home_values.append(home_value)
    hei_caps.append(hei_cap)
    hei_intrinsic_values.append(hei_intrinsic_value)
    settlement_values.append(settlement_value)

# Create DataFrame for clarity
df = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values,
})

# Metrics
col1, col2 = st.columns(2)
col1, col2 = st.columns(2)

with col1:
    st.metric("Premium Amount", f"${premium_amount:,.0f}")
with col2:
    st.metric("Investor Percentage", f"{investor_pct * 100:.0f}%")

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name='Home Value', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name='HEI Cap', line=dict(color='red')))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name='HEI Intrinsic Value', line=dict(color='orange')))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name='Settlement Value', fill='tozeroy', line=dict(color='green')))

fig.update_layout(title="HEI Calculation Over 10 Years", xaxis_title="Year", yaxis_title="Value ($)", height=500)
st.plotly_chart(fig, use_container_width=True)

# Display Table
st.subheader("Annual HEI Breakdown")
df_display = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values
})

st.dataframe(df_results.style.format("${:,.0f}"), use_container_width=True)
