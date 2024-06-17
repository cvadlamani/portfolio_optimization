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

    current_date = pd.to_datetime(current_date)
    in_sample_start_date = current_date - datetime.timedelta(days=IN_SAMPLE_DAYS)
    in_sample_end_date  = current_date - datetime.timedelta(days=1)

    file_path = r"C:\\Users\\Chitra Vadlamani\Desktop\\githubrepo\\portfolio_optimization\\company_stock_data.csv"
    df = pd.read_csv(file_path)

    stocks = list(set(df["Symbol"]))

    in_sample_returns_df = get_stock_returns(stocks, in_sample_start_date, in_sample_end_date )
    in_sample_returns_df = in_sample_returns_df.sort_values("Date")
    in_sample_returns_df = in_sample_returns_df.fillna(method="ffill").fillna(0)

    Hamiltonian_matrix = get_hamiltonian(in_sample_returns_df, stocks, in_sample_start_date, in_sample_end_date )

    selected_stocks = optimize_portfolio(Hamiltonian_matrix, stocks)


    selected_stocks_df = pd.DataFrame()
    selected_stocks_df["Date"] = [current_date] * len(selected_stocks)
    selected_stocks_df["Stock"] = selected_stocks
    

    if os.path.exists(SEL_STOCK_OUT_FILE):
        selected_stocks_df.to_csv(
            SEL_STOCK_OUT_FILE, index=False, mode="a", header=False,
        )
    else:
        selected_stocks_df.to_csv(
            SEL_STOCK_OUT_FILE, index=False,
        )

    

    print("Optimized portfolio contains the following stocks:")
    display(HTML(selected_stocks_df[["Stock"]].tail(1).to_html()))

    return selected_stocks_df