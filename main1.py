import os
import pandas as pd
import datetime
from run import run
from parameters import OUT_OF_SAMPLE_DAYS, DROP_STOCKS,stock_df

# Import libs                                                                                 
import os
import pandas as pd
import yfinance as yf

# Define some parameters                                                                                            
OUT_DIR = "data"
if not os.path.exists(OUT_DIR):
    # Create the directory
    os.makedirs(OUT_DIR)

DROP_STOCKS = []

# Get the list of all existing stocks                                                         
stocks = list(stock_df["Symbol"].unique()) + ["NDX", "QQQE"] 

for stock in stocks:
    try:
        tmp_df = yf.Ticker(stock).history(
            period="max", interval="1d",
        )[["Close"]].rename(
            columns={
                "Close": stock,
            }
        )
        tmp_df["Date"] = tmp_df.index
        tmp_df.to_csv(
            os.path.join(OUT_DIR, "%s.csv" % stock),
            index=False,
        )
    except Exception as exc:
        print("Could not get price for %s" % stock)
        print(exc)
        DROP_STOCKS.append(stock)

    if tmp_df.shape[0] == 0:
        DROP_STOCKS.append(stock)


min_date = pd.to_datetime("2022-01-13")                                    
max_date = pd.to_datetime("2022-04-30")

SEL_STOCK_OUT_FILE = "selected_stocks.csv"

curr_date = min_date
while curr_date < max_date:
    tmp_sel_stock_df = run(curr_date)

    if os.path.exists(SEL_STOCK_OUT_FILE):
        tmp_sel_stock_df.to_csv(
            SEL_STOCK_OUT_FILE, index=False, mode="a", header=False,
        )
    else:
        tmp_sel_stock_df.to_csv(
            SEL_STOCK_OUT_FILE, index=False,
        )

    curr_date += datetime.timedelta(days=OUT_OF_SAMPLE_DAYS + 1)


# Import libs                                                                                 
import sys
import datetime
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# Set params                                                                                  
INIT_PORT_VAL = 1000000.0
OUT_OF_SAMPLE_DAYS = 30
K_PRIME = 30
XI = 5.0
IND_SYMBOL_1 = "QQQE"
IND_SYMBOL_2 = "NDX"

SEL_STOCK_FILE = "selected_stocks.csv"
INDEX_FILE_1 = "data/%s.csv" % IND_SYMBOL_1
INDEX_FILE_2 = "data/%s.csv" % IND_SYMBOL_2

MIN_DATE = pd.to_datetime("2022-01-01")
MAX_DATE = pd.to_datetime("2022-12-31")

# Read allocation file                                                                        
df = pd.read_csv(SEL_STOCK_FILE)
#df["Date"] = df["Date"].astype("datetime64[ns]")
df["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in df["Date"]])
df = df[(df["Date"] >= MIN_DATE) & (df["Date"] <= MAX_DATE)]

# Loop through dates and calculate port value                                                 
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

    stocks = list(set(stocks) - set(DROP_STOCKS) - {"FISV"})
    
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


    





# note these are the results when the beg price assertion from the previous cell was commented, turn into all NaN values
# Plot    
out_df = pd.DataFrame({"Date": dates, "Port_Val": port_vals})
out_df["Date"] = out_df["Date"].astype("datetime64[ns]")
ind_df_1 = pd.read_csv(INDEX_FILE_1)
#ind_df_1["Date"] = ind_df_1["Date"].astype("datetime64[ns]")
ind_df_1["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in ind_df_1["Date"]])
min_date = out_df["Date"].min()
max_date = out_df["Date"].max()
ind_df_1 = ind_df_1[
    (ind_df_1["Date"] >= min_date) & (ind_df_1["Date"] <= max_date)
]
ind_vals_1 = np.array(ind_df_1[IND_SYMBOL_1])
fct = INIT_PORT_VAL / ind_vals_1[0]
ind_vals_1 *= fct

ind_df_2 = pd.read_csv(INDEX_FILE_2)
#ind_df_2["Date"] = ind_df_2["Date"].astype("datetime64[ns]")
ind_df_2["Date"] = pd.to_datetime([pd.Timestamp(timestamp).date() for timestamp in ind_df_2["Date"]])
min_date = out_df["Date"].min()
max_date = out_df["Date"].max()
ind_df_2 = ind_df_2[
    (ind_df_2["Date"] >= min_date) & (ind_df_2["Date"] <= max_date)
]
ind_vals_2 = np.array(ind_df_2[IND_SYMBOL_2])
fct = INIT_PORT_VAL / ind_vals_2[0]
ind_vals_2 *= fct

plt.plot(
    out_df["Date"], out_df["Port_Val"],                                            
    ind_df_1["Date"], ind_vals_1,
    ind_df_2["Date"], ind_vals_2,
)
plt.xlabel("Date")
plt.ylabel("Portfolio Value")

plt.legend(
    [
        "Equal weighted optimal portfolio",                  
        "Equal weighted Nasdaq 100",
        "Nasdaq 100",
    ]
)                                 
plt.show()