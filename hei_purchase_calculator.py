import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏡 Home Equity Investment (HEI) Calculator")

# Sidebar for user inputs with clear formatting
with st.sidebar:
    st.header("📌 Input Parameters")

    home_value = st.number_input(
        "Home Value ($)", min_value=0, value=1_000_000, step=10_000, format="%d"
    )
    appreciation_rate = st.number_input(
        "Appreciation Rate (%)", min_value=0.0, value=2.0, step=0.1, format="%.2f"
    ) / 100
    premium_pct = st.number_input(
        "Premium Percentage (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1, format="%.1f"
    ) / 100
    hei_multiplier = st.number_input(
        "HEI Multiplier", min_value=1.0, value=2.0, step=0.1, format="%.1f"
    )
    investor_cap_rate = st.number_input(
        "Investor Cap (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1, format="%.1f"
    ) / 100
    appreciation_rate = st.number_input(
        "Annual Appreciation (%)", min_value=-10.0, max_value=20.0, value=2.0, step=0.1, format="%.1f"
    ) / 100

# Calculations
premium_amount = home_value * premium_pct
investor_percentage = premium_pct = premium_percentage * hei_multiplier
hei_cap = premium_amount = premium_pct * home_value

years = list(range(11))
home_values = [home_value]
hei_caps = [hei_cap := premium_amount]
hei_intrinsic_values = [investor_percentage := premium_pct * hei_multiplier * home_value]
settlement_values = [min(hei_cap, hei_intrinsic_values[0])]

for year in range(1, 11):
    home_value *= (1 + appreciation_rate)
    hei_cap *= (1 + investor_cap_rate)
    hei_intrinsic_value = home_value * investor_percentage
    settlement_value = min(hei_cap, hei_intrinsic_value)

    home_values.append(home_value)
    hei_caps.append(hei_cap)
    hei_intrinsic_values.append(hei_intrinsic_value)
    settlement_values.append(settlement_value)

# Results DataFrame with formatting
results_df = pd.DataFrame({
    'Year': list(range(0, 11)),
    'Home Value': home_values,
    'HEI Cap': hei_caps,
    'HEI Intrinsic Value': hei_intrinsic_values,
    'Settlement Value': settlement_values
})

# Display metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Premium Amount", f"${home_values[0] * premium_pct:,.0f}")
with col2:
    st.metric("Investor Percentage", f"{(premium_pct * hei_multiplier):.0%}")

# Interactive Chart (Similar to your HTML Chart)
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=results_df["Year"], y=results_df["Home Value"], name="Home Value"))
fig.add_trace(go.Scatter(x=results_df["Year"], y=results_df["HEI Cap"], name="HEI Cap"))
fig.add_trace(go.Scatter(x=results_df["Year"], y=results_df["HEI Intrinsic Value"], name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=results_df["Year"], y=results_df["Settlement Value"], name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title='HEI Value Over Time',
    xaxis_title='Year',
    yaxis_title='Value ($)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Table with currency formatting
def currency(x):
    return "${:,.0f}".format(x)

formatted_df = results_df.copy()
formatted_df = formatted_df.style.format({
    "Home Value": "${:,.0f}",
    "HEI Cap": "${:,.0f}",
    "HEI Intrinsic Value": "${:,.0f}",
    "Settlement Value": "${:,.0f}"
}).hide(axis="index")

st.subheader("📊 HEI Annual Breakdown")
st.dataframe(formatted_df, use_container_width=True)

