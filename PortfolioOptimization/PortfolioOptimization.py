import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pyomo.environ as pyo

def main():

    # account for date running
    end_date = input("End date(yyyy-mm-dd):")
    
    # array of ticker symbols
    tickers = getTickers()

    data_dict = {}

    # store ticker data, adjust date if company started > 2010, adjust if no data available
    for ticker in tickers:

        temp_data = yf.download(ticker, start = '2010-01-01', end = end_date, progress=False) 
        
        if temp_data.empty:
            print(f"No data available for {ticker}. It may be delisted or have no price data.")
            continue

        first_valid_date = temp_data.first_valid_index()

        data = yf.download(ticker, start=first_valid_date, end = end_date, progress=False)

        if data.empty:
            print(f"No data available for {ticker} after {first_valid_date}.")
            continue

        # store data in the dictionary
        data_dict[ticker] = data['Adj Close']

    # reformat to one df
    combined_data = pd.concat(data_dict, axis = 1)

    # daily returns for each stock
    returns = combined_data.pct_change().dropna()

    # expected returns (average daily return)
    expected_returns = returns.mean()

    # Calculate covariance matrix (for risk)
    cov_matrix = returns.cov()

    optimize(expected_returns, cov_matrix)


def getTickers():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    # page content
    response = requests.get(url)

    # parse html content
    soup = BeautifulSoup(response.content, 'html.parser')

    # table containing the tickers
    table = soup.find('table', {'class': 'wikitable'})

    tickers = []

    # loop through the rows of the table, skip header, get ticker
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if cols:
            ticker = cols[0].text.strip() 
            tickers.append(ticker)
    
    return tickers


def optimize(expected_returns, cov_matrix):

    # build model
    model = pyo.ConcreteModel()
    tickers = expected_returns.index.tolist()

    # vars
    model.allocations = pyo.Var(tickers, domain = pyo.NonNegativeReals)
    model.selected = pyo.Var(tickers, domain = pyo.Binary)


    # objective function
    def objRule(model):
        return sum(expected_returns[ticker] * model.allocations[ticker] for ticker in tickers)
    model.obj = pyo.Objective(rule = objRule, sense = pyo.maximize)

    # constraints
    # decimals add up to 1 so we have a fractional breakdown
    def sumRule(model):
        return sum(model.allocations[ticker] for ticker in tickers) == 1
    model.sum_const = pyo.Constraint(rule = sumRule)

    # diversified portfolio, thus min of 25 stocks
    def numberStocks(model):
        return sum(model.selected[ticker] for ticker in tickers) >= 25
    model.num_stocks_const = pyo.Constraint(rule = numberStocks)

    # link vars
    def selectionLinkRule(model, ticker):
        return model.allocations[ticker] >= 0.01 * model.selected[ticker]
    model.link_const = pyo.Constraint(tickers, rule = selectionLinkRule)    

    # volatily < 0.005 -> stdev(0.05) = 7 % variance
    def minVolatility(model):
        return sum(model.allocations[i] * cov_matrix.loc[i, j] * model.allocations[j] for i
                   in tickers for j in tickers) <= 0.005       
    model.min_vol_const = pyo.Constraint(rule = minVolatility)

    # solution
    solver = pyo.SolverFactory("gurobi")
    result = solver.solve(model, tee=True)
    print(f'The solver returned a status of: {result.solver.termination_condition}')
    
    if result.solver.termination_condition == pyo.TerminationCondition.optimal:
        print(f"Optimal value: {pyo.value(model.obj)}")
        print("Optimal allocations:")
        for ticker in tickers:
            if pyo.value(model.allocations[ticker]) > 0:
                print(f"{ticker}: {pyo.value(model.allocations[ticker]):.4f}")

              

main()
