import streamlit as st
import pandas as pd

st.title("Home Equity Investment (HEI) Calculator")

# Input fields
home_value = st.number_input("Home Value ($)", value=1000000, step=5000, format="%d")
home_price_appreciation = st.number_input("Home Price Appreciation (%)", value=2.0, step=0.1, format="%.2f") / 100
premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=0.1) / 100
hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1)
investor_cap = st.number_input("Investor Cap (%)", value=20.0, step=0.1) / 100

# Initial calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

st.markdown(f"**Premium Amount:** ${premium_amount:,.2f}")
st.markdown(f"**Investor Percentage:** {(investor_percentage := premium_percentage * hei_multiplier) * 100:.2f}%")

# Data calculation
years = list(range(11))
data = []
current_home_value = home_value
hei_cap = premium_amount = home_value * premium_percentage

for year in years:
    hei_intrinsic_value = investor_percentage * current_home_value
    settlement_value = min(hei_cap, hei_intrinsic_value := investor_percentage * current_home_value)

    data.append({
        'Year': year,
        'Home Value': round(current_home_value, 2),
        'HEI Cap': round(hei_cap, 2),
        'HEI Intrinsic Value': round(hei_intrinsic_value := investor_percentage * current_home_value, 2),
        'Settlement Value': round(settlement_value, 2)
    })

    hei_cap *= (1 + investor_cap)
    current_home_value *= (1 + (home_price_appreciation))

# Create and style dataframe
df = pd.DataFrame(data)

def highlight_values(row):
    highlight = 'background-color: #90ee90;'
    return [
        '',
        '',
        highlight if (highlight := 'background-color: #90ee90;' if row['HEI Cap'] < row['HEI Intrinsic Value'] else '') else '',
        highlight if (highlight := 'background-color: #90ee90;' if row['HEI Intrinsic Value'] <= row['HEI Cap'] else '') else '',
        ''
    ]

st.dataframe(pd.DataFrame(data).style.apply(highlight, axis=1))

# Chart
chart_df = pd.DataFrame({
    'Year': years,
    'Home Value': df_home := df['Home Value'],
    'HEI Cap': df_cap := df['HEI Cap'],
    'HEI Intrinsic Value': df_intrinsic := df['HEI Intrinsic Value'],
    'Settlement Value': df_settlement := df['Settlement Value']
}).set_index('Year')

st.line_chart(chart_data.set_index('Year'))
