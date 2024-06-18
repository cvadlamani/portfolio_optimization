def get_stock_returns(stocks, min_date, max_date):
    import pandas as pd
    from parameters import stock_df # Importing stock_df from parameters.py

    # Convert min_date and max_date to datetime objects
    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)

    return_df = None # Initialize return dataframe

    # Loop through each stock symbol
    for stock in stocks:
        # Construct file path for each stock's CSV data
        file_path = r"C:\\Users\\Chitra Vadlamani\Desktop\\portfolio_optimization\data/%s.csv" % stock
        # Read stock data from CSV file into DataFrame
        stock_df = pd.read_csv(file_path)
        
        # Convert 'Date' column to datetime format
        stock_df["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in stock_df["Date"]])  
        
        # Fill missing values by carrying forward the last known value (ffill), and then backward filling any remaining missing values (bfill)
        stock_df = stock_df.fillna(method="ffill").fillna(method="bfill")
        
        # Calculate daily percentage change in stock price
        stock_df[stock] = stock_df[stock].pct_change()
        # Drop rows with NaN values (resulting from percentage change calculation)
        stock_df = stock_df.dropna()

        # Filter stock data within the specified min_date and max_date range
        stock_df = stock_df[
            (stock_df["Date"] >= min_date) & (stock_df["Date"] <= max_date)
        ]
        
        # Merge current stock's data into return_df using outer join
        if return_df is None:
            return_df = stock_df
        else:
            return_df = return_df.merge(stock_df, how="outer", on="Date",)
    # Fill any remaining missing values in return_df after merging
    return_df = return_df.fillna(method="ffill").fillna(method="bfill")

    return return_df # Return the final DataFrame containing stock returns