def get_stock_returns(stocks, min_date, max_date):
    import pandas as pd
    from parameters import stock_df

    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)
    return_df = None

    for stock in stocks:
        file_path = r"C:\\Users\\Chitra Vadlamani\Desktop\\portfolio_optimization\data/%s.csv" % stock
        stock_df = pd.read_csv(file_path)
        stock_df["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in stock_df["Date"]])  
        stock_df = stock_df.fillna(method="ffill").fillna(method="bfill")
        stock_df[stock] = stock_df[stock].pct_change()
        stock_df = stock_df.dropna()

        stock_df = stock_df[
            (stock_df["Date"] >= min_date) & (stock_df["Date"] <= max_date)
        ]
        
        if return_df is None:
            return_df = stock_df
        else:
            return_df = return_df.merge(stock_df, how="outer", on="Date",)

    return_df = return_df.fillna(method="ffill").fillna(method="bfill")

    return return_df