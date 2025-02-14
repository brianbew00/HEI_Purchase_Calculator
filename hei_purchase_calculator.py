import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt

def calculate_forecast(home_value, appreciation, origination_date, months=120):
    """
    Forecast the home's value month-by-month using:
      Home Value = home_value * (1 + appreciation)^(month / 12)
    where appreciation is in decimal form.
    
    Returns a DataFrame with:
      - The index labeled as "Month"
      - Columns: Date, Forecasted HEI Value
    """
    data = []
    for m in range(months + 1):
        forecasted_value = home_value * ((1 + appreciation) ** (m / 12))
        forecast_date = pd.to_datetime(origination_date) + pd.DateOffset(months=m)
        formatted_date = forecast_date.strftime('%m/%d/%Y')  # MM/DD/YYYY
        data.append((formatted_date, forecasted_value))
    df = pd.DataFrame(data, columns=["Date", "Forecasted HEI Value"])
    df.index.name = "Month"
    return df

st.title("HEI Forecast Calculator")

with st.form(key="forecast_form"):
    st.subheader("Primary Inputs")
    col1, col2, col3 = st.columns(3)
    with col1:
        home_value = st.number_input("Home Value ($)", value=1000000.0, step=1000.0)
    with col2:
        appreciation_input = st.number_input("Appreciation Rate (Annual %)", value=3.0, step=0.1)
    with col3:
        origination_date_str = st.text_input("Origination Date (MM/DD/YYYY)", value="12/11/2023")
        try:
            origination_date = datetime.datetime.strptime(origination_date_str, "%m/%d/%Y").date()
        except ValueError:
            st.error("Date must be in MM/DD/YYYY format")
            st.stop()
    appreciation = appreciation_input / 100.0

    st.subheader("Option & Investor Inputs")
    col1, col2, col3 = st.columns(3)
    with col1:
        original_hei_amount = st.number_input("Original HEI Amount ($)", value=200000.0, step=1000.0)
    with col2:
        multiplier = st.number_input("Multiplier", value=2.0, step=0.1)
    with col3:
        investor_cap_input = st.number_input("Investor Cap (%)", value=20.0, step=0.1)
    investor_cap = investor_cap_input / 100.0

    st.subheader("Secondary Market Investment Inputs")
    col_acq, col_disp = st.columns(2)
    with col_acq:
        st.markdown("#### Acquisition")
        acq_premium_input = st.number_input("Acquisition Premium / Discount (%)", value=6.0, step=0.1)
        acq_premium = acq_premium_input / 100.0
        acq_method = st.radio("Determine acquisition by:", options=["Contract Age (months)", "Purchase Date"], key="acq_method")
        if acq_method == "Contract Age (months)":
            sec_contract_age = st.number_input("Contract Age (months)", value=4, step=1)
            sec_purchase_date = None
        else:
            sec_purchase_date = st.date_input("Secondary Purchase Date", value=datetime.date(2024, 12, 11), key="acq_date")
            sec_contract_age = None
    with col_disp:
        st.markdown("#### Disposition")
        disp_premium_input = st.number_input("Disposition Premium / (Discount) (%)", value=6.0, step=0.1)
        disp_premium = disp_premium_input / 100.0
        disp_method = st.radio("Determine disposition by:", options=["Hold Period (months)", "Sale Date"], key="disp_method")
        if disp_method == "Hold Period (months)":
            hold_period_months = st.number_input("Hold Period (months)", value=18, step=1)
            sale_date = None
        else:
            sale_date = st.date_input("Sale Date", value=datetime.date(2029, 12, 11), key="disp_date")
            hold_period_months = None

    submitted = st.form_submit_button(label="Generate 120-Month Forecast")

if submitted:
    # Compute forecast.
    forecast_df = calculate_forecast(home_value, appreciation, origination_date, months=120)
    
    # Calculate Contract Value.
    option_value_multiplier = (original_hei_amount / home_value) * multiplier
    forecast_df["Option Value"] = forecast_df["Forecasted HEI Value"] * option_value_multiplier
    
    # Calculate Investor Cap.
    forecast_df["Investor Cap Value"] = original_hei_amount * ((1 + investor_cap) ** (forecast_df.index / 12))
    
    # Rename columns.
    forecast_df.rename(columns={
        "Forecasted HEI Value": "Home Value",
        "Option Value": "Contract Value",
        "Investor Cap Value": "Investor Cap"
    }, inplace=True)
    
    # Add Discount.
    forecast_df["Discount"] = forecast_df.apply(lambda row: max(1 - (row["Investor Cap"] / row["Contract Value"]), 0), axis=1)
    
    # Add Settlement Value.
    forecast_df["Settlement Value"] = np.minimum(forecast_df["Contract Value"], forecast_df["Investor Cap"])
    
    # Compute Acquisition Values.
    forecast_df["Secondary Market Value - Acquisition"] = forecast_df["Settlement Value"] * (1 + acq_premium)
    forecast_df["Secondary Market Investment (Acquisition)"] = 0.0
    if acq_method == "Contract Age (months)":
        target_month_acq = int(sec_contract_age)
    else:
        forecast_dates = pd.to_datetime(forecast_df["Date"], format="%m/%d/%Y")
        target_month_acq = forecast_dates[forecast_dates >= pd.to_datetime(sec_purchase_date)].index.min()
        if pd.isna(target_month_acq):
            target_month_acq = forecast_df.index[-1]
    forecast_df.loc[target_month_acq, "Secondary Market Investment (Acquisition)"] = \
        forecast_df.loc[target_month_acq, "Secondary Market Value - Acquisition"]
    
    # Compute Disposition Values.
    forecast_df["Secondary Market Value (Disposition)"] = forecast_df["Settlement Value"] * (1 + disp_premium)
    forecast_df["Secondary Market Investment (Disposition)"] = 0.0
    if disp_method == "Hold Period (months)":
        target_month_disp = int(target_month_acq) + int(hold_period_months)
    else:
        forecast_dates = pd.to_datetime(forecast_df["Date"], format="%m/%d/%Y")
        target_month_disp = forecast_dates[forecast_dates >= pd.to_datetime(sale_date)].index.min()
        if pd.isna(target_month_disp):
            target_month_disp = forecast_df.index[-1]
    forecast_df.loc[target_month_disp, "Secondary Market Investment (Disposition)"] = \
        forecast_df.loc[target_month_disp, "Secondary Market Value (Disposition)"]
    
    # Rename secondary market columns to shorter labels.
    forecast_df.rename(columns={
        "Secondary Market Value - Acquisition": "Acquisition (Value)",
        "Secondary Market Investment (Acquisition)": "Acquisition (Investment)",
        "Secondary Market Value (Disposition)": "Disposition (Value)",
        "Secondary Market Investment (Disposition)": "Disposition (Investment)"
    }, inplace=True)
    
    # Add new column for First Investor Return.
    forecast_df["First Investor Return"] = np.nan
    acq_invest = forecast_df.loc[target_month_acq, "Acquisition (Investment)"]
    for i in range(target_month_acq + 1, target_month_disp + 1):
        months_held = i - target_month_acq
        forecast_df.loc[i, "First Investor Return"] = (forecast_df.loc[i, "Disposition (Value)"] / acq_invest) ** (12 / months_held) - 1

    # Add new column for Second Investor Return.
    forecast_df["Second Investor Return"] = np.nan
    second_acq = forecast_df.loc[target_month_disp, "Disposition (Investment)"]
    for i in range(target_month_disp + 1, forecast_df.index[-1] + 1):
        months_held = i - target_month_disp
        forecast_df.loc[i, "Second Investor Return"] = (forecast_df.loc[i, "Settlement Value"] / second_acq) ** (12 / months_held) - 1

    # Create a datetime column for charting.
    forecast_df["Date_dt"] = pd.to_datetime(forecast_df["Date"], format="%m/%d/%Y")
    
    st.session_state.forecast_df = forecast_df.copy()
    st.session_state.target_month_acq = target_month_acq
    st.session_state.target_month_disp = target_month_disp

if "forecast_df" in st.session_state:
    forecast_df = st.session_state.forecast_df.copy()
    forecast_df_reset = forecast_df.reset_index()  # "Month" column available.
    
    chart_view = st.selectbox("Select Chart View", ["Investor Returns", "Contract Metrics"])
    
    if chart_view == "Investor Returns":
        # Limit to rows from target_month_acq to 120.
        returns_df = forecast_df_reset[["Month", "Date", "First Investor Return", "Second Investor Return"]].melt(
            id_vars=["Month", "Date"], var_name="Return Type", value_name="Return"
        )
        target_month_acq = st.session_state.target_month_acq
        returns_df = returns_df[(returns_df["Month"] >= target_month_acq) & (returns_df["Month"] <= 120)]
        returns_df = returns_df[returns_df["Return"].notnull()]
        chart_returns = alt.Chart(returns_df).mark_bar().encode(
            x=alt.X("Month:Q", title="Month", scale=alt.Scale(domain=[target_month_acq, 120])),
            y=alt.Y("Return:Q", title="Annualized Return", 
                    axis=alt.Axis(format=".2%", labelFontSize=12, titleFontSize=12, labelPadding=20, titlePadding=0)),
            color=alt.Color("Return Type:N", title=""),
            tooltip=[alt.Tooltip("Month:Q", title="Month"),
                     alt.Tooltip("Date:N", title="Date"),
                     alt.Tooltip("Return:Q", title="Return", format=".2%")]
        ).properties(height=400, width=1200)
        chart_returns = chart_returns.configure_legend(orient='top')
        st.altair_chart(chart_returns, use_container_width=True)
    else:
        metrics_df = forecast_df_reset[["Month", "Date", "Contract Value", "Investor Cap", "Settlement Value"]].melt(
            id_vars=["Month", "Date"], var_name="Metric", value_name="Value"
        )
        chart_metrics = alt.Chart(metrics_df).mark_line().encode(
            x=alt.X("Month:Q", title="Month"),
            y=alt.Y("Value:Q", title="Value ($)", 
                    axis=alt.Axis(format="$,s", labelFontSize=12, titleFontSize=12, labelPadding=20, titlePadding=0)),
            color=alt.Color("Metric:N", title=""),
            tooltip=[alt.Tooltip("Month:Q", title="Month"),
                     alt.Tooltip("Date:N", title="Date"),
                     alt.Tooltip("Value:Q", title="Value", format="$,.2f")]
        ).properties(height=400, width=1200)
        chart_metrics = chart_metrics.configure_legend(orient='top')
        st.altair_chart(chart_metrics, use_container_width=True)
    
    table_df = forecast_df.drop(columns=["Date_dt"])
    st.write("### 120-Month HEI Forecast")
    st.dataframe(
        table_df.style.format({
            "Home Value": "$ {:,.2f}",
            "Contract Value": "$ {:,.2f}",
            "Investor Cap": "$ {:,.2f}",
            "Discount": "{:.2%}",
            "Settlement Value": "$ {:,.2f}",
            "Acquisition (Value)": "$ {:,.2f}",
            "Acquisition (Investment)": "$ {:,.2f}",
            "Disposition (Value)": "$ {:,.2f}",
            "Disposition (Investment)": "$ {:,.2f}",
            "First Investor Return": "{:.2%}",
            "Second Investor Return": "{:.2%}"
        })
    )
