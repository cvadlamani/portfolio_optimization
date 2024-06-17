def run(curr_date):
    import pandas as pd
    import datetime
    from parameters import IN_SAMPLE_DAYS, OUT_OF_SAMPLE_DAYS, DROP_STOCKS
    from get_stock_returns import get_stock_returns
    from get_hamiltonian import get_hamiltonian
    from optimize_portfolio import optimize_portfolio


    print("Processing curr date:", curr_date)

    curr_date = pd.to_datetime(curr_date)
    min_ins_date = curr_date - datetime.timedelta(days=IN_SAMPLE_DAYS)
    max_ins_date = curr_date - datetime.timedelta(days=1)
    min_oos_date = curr_date
    max_oos_date = curr_date + datetime.timedelta(days=OUT_OF_SAMPLE_DAYS)

    file_path = r"C:\\Users\\Chitra Vadlamani\Desktop\\portfolio_optimization\\company_stock_data.csv"
    df = pd.read_csv(file_path)

    stocks = list(set(df["Symbol"]) - set(DROP_STOCKS))

    ins_return_df = get_stock_returns(stocks, min_ins_date, max_ins_date)
    oos_return_df = get_stock_returns(stocks, min_oos_date, max_oos_date)

    ins_return_df = ins_return_df.sort_values("Date")
    ins_return_df = ins_return_df.fillna(method="ffill").fillna(0)

    oos_return_df = oos_return_df.sort_values("Date")
    oos_return_df = oos_return_df.fillna(method="ffill").fillna(0)

    H = get_hamiltonian(ins_return_df, stocks, min_ins_date, max_ins_date)

    sol, sel_stocks = optimize_portfolio(H, stocks, curr_date)

    sel_stock_df = pd.DataFrame()
    sel_stock_df["Date"] = [curr_date] * len(sel_stocks)
    sel_stock_df["Stock"] = sel_stocks

    return sel_stock_df