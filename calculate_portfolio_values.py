

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
    INIT_PORT_VAL = 1000000.0
    OUT_OF_SAMPLE_DAYS = 30

    MIN_DATE = pd.to_datetime("2022-01-01")
    MAX_DATE = pd.to_datetime("2022-12-31")

    df["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in df["Date"]])
    df = df[(df["Date"] >= MIN_DATE) & (df["Date"] <= MAX_DATE)]

    beg_port_val = INIT_PORT_VAL
    df = df.sort_values("Date")
    adj_dates = sorted(df["Date"].unique())
    num_adj_dates = len(adj_dates)
    dates = None
    port_vals = None


    for i in range(num_adj_dates):

        print(
            "Processing adjustment date %s"
            % pd.to_datetime(adj_dates[i]).strftime("%Y-%m-%d")
        )

        beg_date = pd.to_datetime(adj_dates[i])
        if i < num_adj_dates - 1:
            end_date = pd.to_datetime(adj_dates[i + 1])
        else:
            end_date = beg_date + datetime.timedelta(days=OUT_OF_SAMPLE_DAYS)

        tmp_df = df[df["Date"] == beg_date]
        stocks = tmp_df["Stock"]
        stocks = list(set(stocks))

        stocks = list(set(stocks) - {"FISV"})
        
        if end_date > pd.to_datetime("2023-10-20"):
            stocks = list(set(stocks) - {"ATVI"})

        all_dates = [beg_date]
        date0 = beg_date
        while date0 < end_date:
            date0 = date0 + datetime.timedelta(days=1)
            all_dates.append(date0)

        price_df = pd.DataFrame({"Date": all_dates})

        for stock in stocks:
            stock_df = pd.read_csv("data/%s.csv" % stock)
            #stock_df["Date"] = stock_df["Date"].astype("datetime64[ns]")
            stock_df["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in stock_df["Date"]])
            stock_df = stock_df[
                (stock_df["Date"] >= beg_date) & (stock_df["Date"] <= end_date)
            ]

            if price_df is None:
                price_df = stock_df
            else:
                price_df = price_df.merge(stock_df, on="Date", how="outer")

        price_df = price_df.fillna(method="ffill").fillna(method="bfill")
        price_df = price_df.sort_values("Date")

        tmp_dates = np.array(price_df["Date"])
        tmp_port_vals = np.zeros(shape=(price_df.shape[0]))

        assert price_df.shape[0] > 0

        for stock in stocks:
            prices = np.array(price_df[stock])
            beg_price = prices[0]
            stock_wt = 1.0 / len(stocks)

            if beg_price <= 0:
                print(stock)
                print(price_df[["Date", stock]])
                
            assert beg_price > 0, "Error in data for %s" % stock # this assertion was failing, when I comment it out we get all NaN values

            stock_count = stock_wt * beg_port_val / beg_price
            tmp_port_vals += stock_count * prices

        if dates is None:
            dates = tmp_dates
        else:
            dates = np.concatenate([dates, tmp_dates])

        if port_vals is None:
            port_vals = tmp_port_vals
        else:
            port_vals = np.concatenate([port_vals, tmp_port_vals])

        beg_port_val = port_vals[-1]