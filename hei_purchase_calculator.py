import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Streamlit page setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏠 Home Equity Investment (HEI) Calculator")

# Sanity Check (shows your latest deployment)
st.success("✅ The latest version of the app has been loaded.")

# Sidebar Inputs
with st.sidebar:
    st.header("📌 Input Parameters")

    home_value = st.number_input("Home Value ($)", value=1_000_000, step=10_000, format="%d")
    appreciation_rate = st.number_input("Annual Appreciation (%)", value=2.0, step=0.1, format="%.2f") / 100
    premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=0.1, format="%.2f") / 100
    hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1)
    investor_cap_rate = st.number_input("Investor Cap (%)", value=20.0, step=0.1, format="%.2f") / 100

# Calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier
hei_cap = premium_amount

years = list(range(11))
home_values = []
hei_caps = []
hei_intrinsic_values = []
settlement_values = []

current_home_value = home_value

for year in years:
    if year > 0:
        current_home_value = home_values[-1] * (1 + appreciation_rate)
        hei_cap *= (1 + investor_cap_rate)
    else:
        current_home_value = home_value

    hei_intrinsic_value = current_home_value * investor_percentage
    settlement_value = min(hei_cap, hei_intrinsic_value)

    home_values.append(current_home_value)
    hei_caps.append(hei_cap)
    hei_intrinsic_values.append(hei_intrinsic_value)
    settlement_values.append(settlement_value)

    current_home_value *= (1 + appreciation_rate)
    hei_cap *= (1 + investor_cap_rate)

# Create DataFrame
results_df = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values,
})

# Display calculated Premium Amount and Investor Percentage
col1, col2 = st.columns(2)
with col1:
    st.metric("🏷️ Premium Amount", f"${premium_amount:,.0f}")
with col2:
    st.metric("📈 Investor Percentage", f"{investor_percentage:.0%}")

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value"))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap"))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title='HEI Value Over Time',
    xaxis_title='Year',
    yaxis_title='Value ($)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Format DataFrame for display
formatted_df = results_df.copy()
formatted_df["Home Value"] = formatted_df["Home Value"].apply(lambda x: f"${x:,.0f}")
formatted_df["HEI Cap"] = formatted_df["HEI Cap"].apply(lambda x: f"${x:,.0f}")
formatted_df["HEI Intrinsic Value"] = formatted_df["HEI Intrinsic Value"].apply(lambda x: f"${x:,.0f}")
formatted_df["Settlement Value"] = formatted_df["Settlement Value"].apply(lambda x: f"${x:,.0f}")

st.subheader("📊 HEI Annual Breakdown")
st.dataframe(formatted_df.set_index("Year"), use_container_width=True)
