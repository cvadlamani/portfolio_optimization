
def fetch_data():
    import os
    import pandas as pd
    import yfinance as yf
    from parameters import stock_df

    # Define output directory
    OUT_DIR = "data"
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    
    DROP_STOCKS = []
    
    # Get the list of all existing stocks
    stocks = list(stock_df["Symbol"].unique()) + ["NDX", "QQQE"]
    
    for stock in stocks:
        csv_filename = os.path.join(OUT_DIR, "%s.csv" % stock)
        
        # Check if CSV file already exists
        if os.path.isfile(csv_filename):
            print(f"Fetched {stock} data.")
            continue
        
        try:
            # Fetch historical data
            tmp_df = yf.Ticker(stock).history(
                period="max", interval="1d",
            )[["Close"]].rename(
                columns={
                    "Close": stock,
                }
            )
            
            # Prepare CSV file
            tmp_df["Date"] = tmp_df.index
            tmp_df.to_csv(
                csv_filename,
                index=False,
            )
        
        except Exception as exc:
            print(f"Could not get price for {stock}")
            print(exc)
            DROP_STOCKS.append(stock)
        
        if tmp_df.shape[0] == 0:
            DROP_STOCKS.append(stock)
    
    

