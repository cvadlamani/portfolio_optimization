def get_hamiltonian(
    return_df, stocks, min_date, max_date,
):
    import numpy as np
    import datetime
    from parameters import WINDOW_DAYS, WINDOW_OVERLAP_DAYS, XI
    import pandas as pd

    K = len(stocks)

    # Calculate P and Q                                                                       
    Q = np.zeros(shape=(K, K), dtype="d")
    P = np.zeros(shape=(K, K), dtype="d")
    m = 0
    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)
    tmp_date = min_date
    while tmp_date <= max_date:
        tmp_min_date = tmp_date
        tmp_max_date = tmp_date + datetime.timedelta(days=WINDOW_DAYS)
        tmp_df = return_df[
            (return_df["Date"] >= tmp_min_date)
            & (return_df["Date"] <= tmp_max_date)
        ]
        r_list = []
        for i in range(K):
            r_list.append(np.array(tmp_df[stocks[i]]))

        Q += np.cov(r_list)

        for i in range(K):
            for j in range(K):
                P[i][j] += np.mean(r_list[i]) * np.mean(r_list[j])

        tmp_date += datetime.timedelta(
            days=WINDOW_DAYS - WINDOW_OVERLAP_DAYS,
        )
        m += 1

    fct = m
    if fct > 0:
        fct = 1.0 / fct

    P = fct * P
    Q = fct * Q

    # Calculate the Hamiltonian                                                              
    H = -P + XI * Q

    # make sure H is symmetric up to machine precision                                       
    H = 0.5 * (H + H.transpose())

    return H