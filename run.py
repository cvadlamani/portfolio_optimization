'''
The run function is designed to perform portfolio optimization based on historical stock data. 
It calculates in-sample and out-of-sample returns, constructs a Hamiltonian matrix to balance 
returns and risks, and selects the optimal set of stocks for a given current date. The function
ultimately returns a DataFrame of the selected stocks and the date on which the selection was made.
'''


def run(current_date):
    import pandas as pd
    import datetime
    from parameters import IN_SAMPLE_DAYS, OUT_OF_SAMPLE_DAYS
    from get_stock_returns import get_stock_returns
    from get_hamiltonian import get_hamiltonian
    from optimize_portfolio import optimize_portfolio


    print("current date being processed for portfolio optimization:", current_date )
    
    '''
    Converts the current date to a datetime object and calculates the start and end dates for the in-sample 
    and out-of-sample periods based on the IN_SAMPLE_DAYS and OUT_OF_SAMPLE_DAYS parameters.
    '''
    current_date  = pd.to_datetime(current_date )
    in_sample_start_date  = current_date  - datetime.timedelta(days=IN_SAMPLE_DAYS)
    in_sample_end_date  = current_date  - datetime.timedelta(days=1)
    out_of_sample_start_date  = current_date 
    out_of_sample_end_date  = current_date  + datetime.timedelta(days=OUT_OF_SAMPLE_DAYS)

    #Reads the stock data from a CSV file and extracts a list of unique stock symbols.
    file_path = r"C:\\Users\\Chitra Vadlamani\Desktop\\portfolio_optimization_repo\\company_stock_data.csv"
    df = pd.read_csv(file_path)
    stocks = list(set(df["Symbol"]))

    #Retrieves the stock return data for both the in-sample and out-of-sample periods
    in_sample_returns_df = get_stock_returns(stocks, in_sample_start_date , in_sample_end_date )
    out_of_sample_returns_df = get_stock_returns(stocks, out_of_sample_start_date , out_of_sample_end_date )

    #Sorts the return data by date and fills missing values by carrying forward the last known value (ffill), and then filling any remaining missing values with 0.
    in_sample_returns_df = in_sample_returns_df.sort_values("Date")
    in_sample_returns_df = in_sample_returns_df.fillna(method="ffill").fillna(0)

    out_of_sample_returns_df = out_of_sample_returns_df.sort_values("Date")
    out_of_sample_returns_df = out_of_sample_returns_df.fillna(method="ffill").fillna(0)


    #Calculates the Hamiltonian matrix based on the in-sample return data and the date range.
    hamiltonian_matrix = get_hamiltonian(in_sample_returns_df, stocks, in_sample_start_date , in_sample_end_date )

    #Uses the Hamiltonian matrix to find the optimal set of stocks for the given current date.
    selected_stocks = optimize_portfolio(hamiltonian_matrix, stocks, current_date )

    #Creates a DataFrame to store the selected stocks and the current date.
    selected_stocks_df = pd.DataFrame()
    selected_stocks_df["Date"] = [current_date ] * len(selected_stocks)

    #Returns the DataFrame containing the selected stocks that form the optimized portfolio and the date.
    return selected_stocks_df