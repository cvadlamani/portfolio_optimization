def run(current_date):
    import pandas as pd
    import datetime
    from parameters import IN_SAMPLE_DAYS, SEL_STOCK_OUT_FILE
    from get_stock_returns import get_stock_returns
    from get_hamiltonian import get_hamiltonian
    from optimize_portfolio import optimize_portfolio
    import os
    from IPython.display import display, HTML

    print("Processing curr date:", current_date)

    # Convert current_date to datetime object and define in-sample date range
    current_date = pd.to_datetime(current_date)
    in_sample_start_date = current_date - datetime.timedelta(days=IN_SAMPLE_DAYS)
    in_sample_end_date  = current_date - datetime.timedelta(days=1)

    # Specify the file path to the CSV containing stock data and read it into a DataFrame
    file_path = r"C:\\Users\\Chitra Vadlamani\Desktop\\githubrepo\\portfolio_optimization\\company_stock_data.csv"
    df = pd.read_csv(file_path)

    # Extract unique stock symbols from the DataFrame
    stocks = list(set(df["Symbol"]))

    # Retrieve in-sample returns for the specified date range and preprocess the data
    in_sample_returns_df = get_stock_returns(stocks, in_sample_start_date, in_sample_end_date )
    in_sample_returns_df = in_sample_returns_df.sort_values("Date")
    in_sample_returns_df = in_sample_returns_df.fillna(method="ffill").fillna(0)

    # Generate the Hamiltonian matrix using the in-sample returns and date range
    Hamiltonian_matrix = get_hamiltonian(in_sample_returns_df, stocks, in_sample_start_date, in_sample_end_date )

    # Optimize the portfolio to select the best stocks based on the Hamiltonian matrix
    selected_stocks = optimize_portfolio(Hamiltonian_matrix, stocks)

    # Create a DataFrame to store the selected stocks
    selected_stocks_df = pd.DataFrame()
    selected_stocks_df["Date"] = [current_date] * len(selected_stocks)
    selected_stocks_df["Stock"] = selected_stocks
    
    # Append or create a new CSV file with the selected stocks
    if os.path.exists(SEL_STOCK_OUT_FILE):
        selected_stocks_df.to_csv(
            SEL_STOCK_OUT_FILE, index=False, mode="a", header=False,
        )
    else:
        selected_stocks_df.to_csv(
            SEL_STOCK_OUT_FILE, index=False,
        )

    
    # Display the optimized portfolio stocks 
    print("Optimized portfolio contains the following stocks:")
    display(HTML(selected_stocks_df[["Stock"]].tail(1).to_html()))

    