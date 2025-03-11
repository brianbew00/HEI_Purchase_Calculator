import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏠 Home Equity Investment (HEI) Calculator")

# Sanity Check
st.write("✅ The latest version of the app has been loaded.")

# Sidebar Inputs
with st.sidebar:
    st.header("📌 Input Parameters")
    home_value = st.number_input("Home Value ($)", value=1_000_000, step=10_000)
    appreciation_rate = st.number_input("Appreciation Rate (%)", value=2.0, step=0.1) / 100
    premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=0.1) / 100
    hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1)
    investor_cap_rate = st.number_input("Investor Cap (%)", value=20.0, step=0.1) / 100

# Initial Calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

# Lists to store calculations
years = list(range(11))
home_values = []
hei_caps = []
hei_intrinsic_values = []
settlement_values = []

current_home_value = home_value
current_hei_cap = premium_amount

for year in years:
    if year != 0:
        current_home_value *= (1 + appreciation_rate)
        current_hei_cap *= (1 + investor_cap_rate)
    
    intrinsic_value = current_home_value * investor_percentage
    settlement_value = min(current_hei_cap, hei_intrinsic_value)

    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    hei_intrinsic_values.append(hei_intrinsic_value)
    settlement_values.append(settlement_value)

# Creating DataFrame
results_df = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values,
})

# Display formatted metrics
col1, col2 = st.columns(2)
col1.metric("Premium Amount", f"${premium_amount:,.0f}")
col2.metric("Investor Percentage", f"{investor_percentage:.0%}")

# Plotly Interactive Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value"))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap"))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title='HEI Investment Values Over 10 Years',
    xaxis_title='Year',
    yaxis_title='Value ($)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Formatted DataFrame Display
formatted_df = results_df.copy()
formatted_df["Home Value"] = formatted_df["Home Value"].map("${:,.0f}".format)
formatted_df["HEI Cap"] = formatted_df["HEI Cap"].map("${:,.0f}".format)
formatted_df["HEI Intrinsic Value"] = formatted_df["HEI Intrinsic Value"].map("${:,.0f}".format)
formatted_df["Settlement Value"] = formatted_df["Settlement Value"].map("${:,.0f}".format)

st.subheader("📊 Detailed Annual Breakdown")
st.dataframe(formatted_df.set_index("Year"), use_container_width=True)

# Sanity check to confirm the latest version
st.write("✅ The latest version of the app has been loaded.")
