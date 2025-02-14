metrics_df = forecast_df_reset[["Month", "Date", "Contract Value", "Investor Cap", "Settlement Value"]].melt(
    id_vars=["Month", "Date"], var_name="Metric", value_name="Value"
)
chart_metrics = alt.Chart(metrics_df).mark_line().encode(
    x=alt.X("Month:Q", title="Month"),
    y=alt.Y("Value:Q", title="Value ($)", 
            axis=alt.Axis(format="$,s", labelFontSize=12, titleFontSize=12, labelPadding=10, titlePadding=20)),
    color=alt.Color("Metric:N", title=""),
    tooltip=[
        alt.Tooltip("Month:Q", title="Month"),
        alt.Tooltip("Date:N", title="Date"),
        alt.Tooltip("Value:Q", title="Value", format="$,.2f")
    ]
).properties(height=400, width=1200)

chart_metrics = chart_metrics.configure_legend(orient='top')\
                               .configure_axisY(titleAngle=0, titleAlign="left", titleAnchor="start")
st.altair_chart(chart_metrics, use_container_width=True)
