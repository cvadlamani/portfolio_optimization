def calculate_portfolio_values():
    import sys 
    import datetime
    import warnings
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from parameters import df

    warnings.filterwarnings("ignore")
    
    # Set params                                                                                  
    initial_portfolio_value = 1000000.0
    OUT_OF_SAMPLE_DAYS = 30

    MIN_DATE = pd.to_datetime("2022-01-01")
    MAX_DATE = pd.to_datetime("2022-12-31")

    # Read allocation file                                                                        
    df["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in df["Date"]])
    df = df[(df["Date"] >= MIN_DATE) & (df["Date"] <= MAX_DATE)]

    beginning_portfolio_value = initial_portfolio_value
    df = df.sort_values("Date")
    unique_dates = sorted(df["Date"].unique())
    no_of_unique_dates = len(unique_dates)
    dates = None
    portfolio_values = None


    for i in range(no_of_unique_dates):

        print(
            "Processing adjustment date %s"
            % pd.to_datetime(unique_dates[i]).strftime("%Y-%m-%d")
        )

        beginning_date = pd.to_datetime(unique_dates[i])
        if i < no_of_unique_dates - 1:
            end_date = pd.to_datetime(unique_dates[i + 1])
        else:
            end_date = beginning_date + datetime.timedelta(days=OUT_OF_SAMPLE_DAYS)

        temp_df = df[df["Date"] == beginning_date]
        stocks = temp_df["Stock"]
        stocks = list(set(stocks))

        stocks = list(set(stocks)  - {"FISV"})
        
        if end_date > pd.to_datetime("2023-10-20"):
            stocks = list(set(stocks) - {"ATVI"})

        all_dates = [beginning_date]
        date0 = beginning_date
        while date0 < end_date:
            date0 = date0 + datetime.timedelta(days=1)
            all_dates.append(date0)

        price_df = pd.DataFrame({"Date": all_dates})

        for stock in stocks:
            stock_df = pd.read_csv("data/%s.csv" % stock)
            stock_df["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in stock_df["Date"]])
            stock_df = stock_df[
                (stock_df["Date"] >= beginning_date) & (stock_df["Date"] <= end_date)
            ]

            if price_df is None:
                price_df = stock_df
            else:
                price_df = price_df.merge(stock_df, on="Date", how="outer")

        price_df = price_df.fillna(method="ffill").fillna(method="bfill")
        price_df = price_df.sort_values("Date")

        temp_dates = np.array(price_df["Date"])
        temp_portfolio_values = np.zeros(shape=(price_df.shape[0]))

        assert price_df.shape[0] > 0

        for stock in stocks:
            prices = np.array(price_df[stock])
            beg_price = prices[0]
            stock_wt = 1.0 / len(stocks)

            if beg_price <= 0:
                print(stock)
                print(price_df[["Date", stock]])
                
            assert beg_price > 0, "Error in data for %s" % stock 

            stock_count = stock_wt * beginning_portfolio_value / beg_price
            temp_portfolio_values += stock_count * prices

        if dates is None:
            dates = temp_dates
        else:
            dates = np.concatenate([dates, temp_dates])

        if portfolio_values is None:
            portfolio_values = temp_portfolio_values
        else:
            portfolio_values = np.concatenate([portfolio_values, temp_portfolio_values])

        beginning_portfolio_value = portfolio_values[-1]