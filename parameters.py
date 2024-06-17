import pandas as pd
from IPython.display import display, HTML
import os
import sys
import time
import datetime
import json
import warnings
from functools import wraps
import numpy as np
import pandas as pd
file_path = r"C:\\Users\\Chitra Vadlamani\Desktop\\portfolio_optimization\\company_stock_data.csv"
stock_df = pd.read_csv(file_path)
OUT_DIR = "data"
file_path = r"C:\\Users\\Chitra Vadlamani\Desktop\\portfolio_optimization\\selected_stocks.csv"
df = pd.read_csv(file_path)
DROP_STOCKS = []
stocks = list(stock_df["Symbol"].unique()) + ["NDX", "QQQE"]
min_date = pd.to_datetime("2022-01-13")
max_date = pd.to_datetime("2022-04-30")
SEL_STOCK_OUT_FILE = "selected_stocks.csv"
ALPHA = 1.0 # The coefficient for penalty term (for linear constraint)
N_SAMPLES = 5 # Number of solution samples
XI = 5.0 # The xi variable as defined in Methodology
K_PRIME = 3 # Number of selected stocks
WINDOW_DAYS = 30 # Size of each sliding window in days
WINDOW_OVERLAP_DAYS = 15 # Overlap between sliding windows in days
IN_SAMPLE_DAYS = 180 # Size of the lookback period in days
OUT_OF_SAMPLE_DAYS = 30 # Size of the horizon window in days