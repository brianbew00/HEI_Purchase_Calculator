import pandas as pd
import datetime

def calculate_forecast(home_value, appreciation, origination_date, months=120):
    """
    Forecast the home’s value month-by-month using monthly compounding.
    Returns a DataFrame with the index labeled as "Month", and columns for Date and Forecasted HEI Value.
    """
    data = []
    current_value = home_value
    current_date = pd.to_datetime(origination_date)
    
    # Forecast for each month from 0 to 120 (inclusive; month 0 is the origination)
    for m in range(months + 1):
        data.append((current_date.strftime('%Y-%m-%d'), current_value))
        current_date += pd.DateOffset(months=1)
        current_value *= (1 + appreciation / 12)
    
    # Create a DataFrame with the calculated data
    df = pd.DataFrame(data, columns=["Date", "Forecasted HEI Value"])
    
    # Set the DataFrame index to be the month number and label it "Month"
    df.index.name = "Month"
    
    return df

# Example usage:
origination_date = datetime.date(2023, 12, 11)
forecast_df = calculate_forecast(home_value=1000000.0, appreciation=0.03, origination_date=origination_date, months=120)

# Display the first few rows to verify:
print(forecast_df.head())
