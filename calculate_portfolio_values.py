def calculate_portfolio_values():
    import sys 
    import datetime
    import warnings
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from parameters import df # Importing DataFrame df from parameters.py

    warnings.filterwarnings("ignore")
    
    # Set initial parameters                                                                                
    initial_portfolio_value = 1000000.0 # Starting portfolio value
    OUT_OF_SAMPLE_DAYS = 30 # Number of days for out-of-sample testing

    MIN_DATE = pd.to_datetime("2022-01-01") # Minimum date for data filtering
    MAX_DATE = pd.to_datetime("2022-12-31") # Maximum date for data filtering

    # Read allocation file and filter dates                                                                     
    df["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in df["Date"]])
    df = df[(df["Date"] >= MIN_DATE) & (df["Date"] <= MAX_DATE)]

    beginning_portfolio_value = initial_portfolio_value # Initialize portfolio value
    df = df.sort_values("Date") # Sort DataFrame by date
    unique_dates = sorted(df["Date"].unique()) # Get unique dates from DataFrame
    no_of_unique_dates = len(unique_dates) # Number of unique dates
    dates = None # Initialize dates variable
    portfolio_values = None # Initialize portfolio values variable

    # Loop through each unique date in the DataFrame
    for i in range(no_of_unique_dates):

        print(
            "Processing adjustment date %s"
            % pd.to_datetime(unique_dates[i]).strftime("%Y-%m-%d")
        )

        beginning_date = pd.to_datetime(unique_dates[i]) # Get current date
        if i < no_of_unique_dates - 1:
            end_date = pd.to_datetime(unique_dates[i + 1]) # Get next date
        else:
            end_date = beginning_date + datetime.timedelta(days=OUT_OF_SAMPLE_DAYS)

        temp_df = df[df["Date"] == beginning_date] # Filter DataFrame for current date
        stocks = temp_df["Stock"]  # Get stocks for current date
        stocks = list(set(stocks)) # Remove duplicates from list of stocks

        stocks = list(set(stocks)  - {"FISV"}) # Exclude "FISV" stock if present
        
        # Exclude "ATVI" stock after a specific date
        if end_date > pd.to_datetime("2023-10-20"):
            stocks = list(set(stocks) - {"ATVI"})

        all_dates = [beginning_date] # Initialize list of all dates with current date
        date0 = beginning_date

        # Loop to generate list of all dates between beginning_date and end_date
        while date0 < end_date:
            date0 = date0 + datetime.timedelta(days=1)
            all_dates.append(date0)

        # Create DataFrame with all dates
        price_df = pd.DataFrame({"Date": all_dates})

        # Loop through each stock and merge its price data into price_df
        for stock in stocks:
            stock_df = pd.read_csv("data/%s.csv" % stock) # Read stock data from CSV file
            stock_df["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in stock_df["Date"]]) # Convert 'Date' column to datetime
            stock_df = stock_df[
                (stock_df["Date"] >= beginning_date) & (stock_df["Date"] <= end_date)
            ] # Filter stock data between beginning_date and end_date

            if price_df is None:
                price_df = stock_df # Set price_df to current stock data
            else:
                price_df = price_df.merge(stock_df, on="Date", how="outer") # Merge stock data into price_df

        price_df = price_df.fillna(method="ffill").fillna(method="bfill") # Fill missing values in price_df
        price_df = price_df.sort_values("Date") # Sort price_df by date

        temp_dates = np.array(price_df["Date"])  # Get dates as numpy array
        temp_portfolio_values = np.zeros(shape=(price_df.shape[0])) # Initialize portfolio values array

        assert price_df.shape[0] > 0 # Assert that price_df has data

        # Loop through each stock and calculate portfolio values
        for stock in stocks:
            prices = np.array(price_df[stock]) # Get prices for current stock
            beg_price = prices[0]  # Get beginning price of current stock
            stock_wt = 1.0 / len(stocks) # Calculate stock weight

            if beg_price <= 0: # Check for invalid data (price <= 0)
                print(stock)
                print(price_df[["Date", stock]])
                
            assert beg_price > 0, "Error in data for %s" % stock   # Assert that price is greater than 0

            stock_count = stock_wt * beginning_portfolio_value / beg_price # Calculate stock count
            temp_portfolio_values += stock_count * prices # Update temporary portfolio values

        # Concatenate dates and portfolio values
        if dates is None:
            dates = temp_dates
        else:
            dates = np.concatenate([dates, temp_dates])

        # Concatenate portfolio values
        if portfolio_values is None:
            portfolio_values = temp_portfolio_values
        else:
            portfolio_values = np.concatenate([portfolio_values, temp_portfolio_values])

        beginning_portfolio_value = portfolio_values[-1] # Update beginning portfolio value