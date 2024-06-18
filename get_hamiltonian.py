def get_hamiltonian(
    return_df, stocks, min_date, max_date,
):
    import numpy as np
    import datetime
    from parameters import WINDOW_DAYS, WINDOW_OVERLAP_DAYS, XI
    import pandas as pd

    K = len(stocks) # Number of stocks in the portfolio

    # # Initialize matrices for covariance (Q) and mean-product (P)                                                                     
    Q = np.zeros(shape=(K, K), dtype="d")
    P = np.zeros(shape=(K, K), dtype="d")
    
    # Initialize counters
    m = 0 # Counter for the number of overlapping windows

    # Counter for the number of overlapping windows
    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)
    temp_date = min_date

    # Iterate over overlapping windows of data
    while temp_date <= max_date:
        # Define the start and end dates for the current window
        temp_min_date = temp_date
        temp_max_date = temp_date + datetime.timedelta(days=WINDOW_DAYS)
        
        # Subset the return dataframe to the current window
        temp_df = return_df[
            (return_df["Date"] >= temp_min_date)
            & (return_df["Date"] <= temp_max_date)
        ]

         # Initialize a list to store returns for each stock in the window
        r_list = []
        for i in range(K):
            r_list.append(np.array(temp_df[stocks[i]]))

        # Update the covariance matrix (Q)
        Q += np.cov(r_list)

        # Update the mean-product matrix (P)
        for i in range(K):
            for j in range(K):
                P[i][j] += np.mean(r_list[i]) * np.mean(r_list[j])

        # Move the window forward by (WINDOW_DAYS - WINDOW_OVERLAP_DAYS) days
        temp_date += datetime.timedelta(
            days=WINDOW_DAYS - WINDOW_OVERLAP_DAYS,
        )
        m += 1 # Increment the window counter

    # Normalize P and Q by the number of overlapping windows (m)
    fct = m
    if fct > 0:
        fct = 1.0 / fct

    P = fct * P
    Q = fct * Q

    # # Calculate the Hamiltonian matrix                                                          
    hamiltonian_matrix = -P + XI * Q

    # Ensure the Hamiltonian matrix is symmetric (up to machine precision)                                      
    hamiltonian_matrix = 0.5 * (hamiltonian_matrix + hamiltonian_matrix.transpose())

    return hamiltonian_matrix