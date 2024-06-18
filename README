# Binary Optimization for Portfolio Selection

This repository contains code to perform binary optimization on a portfolio of 5 stocks, selecting an optimized subset of 3 stocks. 

## Dependencies

Before running the code, make sure you have the necessary dependencies installed. You can install them using pip:

pip install pandas
pip install IPython
pip install --upgrade "qci-client<5"

## Python Version

Ensure you are using the appropriate Python version (3.8 or higher) that is compatible with the dependencies listed above.


## QCI Client and API Token

To use the QCI Client, you need to have an API token. Make sure you have your API token ready and set up in the environment. You can use the following link to sign up: https://quantumcomputinginc.com/learn/tutorials-and-use-cases/quick-start-on-cloud

## File and Method Descriptions

### parameters.py

This file contains the parameters used for the optimization process, such as the number of in-sample and out-of-sample days.

### get_stock_returns.py

Contains the method `get_stock_returns` which retrieves stock return data for the specified time periods.

### get_hamiltonian.py

Contains the method `get_hamiltonian` which constructs the Hamiltonian matrix used to balance returns and risks.

### optimize_portfolio.py

Contains the method `optimize_portfolio` which uses the Hamiltonian matrix to find the optimal set of stocks.


### calculate_portfolio_values.py

The function calculates how the value of an investment portfolio changes over time, excluding specific stocks when necessary.


### main.py
Run this file, it ties all the files togeter and outputs the desired portfolio.

### run.py

The `run` function optimizes a stock portfolio based on historical data up to a specified date. It reads stock data, calculates in-sample returns, constructs a Hamiltonian matrix to balance returns and risks, and selects the optimal stocks. The selected stocks are saved to an output CSV file and displayed. The function returns a DataFrame with the selected stocks and the date of optimization.

## Path Files

Make sure the paths to the CSV files containing the stock data are correctly specified in your code. For example:

file_path = r"C:\\Users\\Chitra Vadlamani\Desktop\\portfolio_optimization_repo\\company_stock_data.csv"


