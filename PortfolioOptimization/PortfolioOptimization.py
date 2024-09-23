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
    model = pyo.ConcreteModel()

    # decision variables
    model.x1 = pyo.Var(domain = pyo.NonNegativeReals)
    model.x2 = pyo.Var(domain = pyo.NonNegativeReals)
    model.x3 = pyo.Var()

    # objective function
    def obj_rule(model):
        return 30*model.x1 - 100*model.x2 - 40*model.x3
    model.obj = pyo.Objective(rule = obj_rule, sense = pyo.maximize)

    # constraints
    def rule_one(model):
        return (3*model.x1 + 10*model.x2 + 5*model.x3) <= 40
    model.rule_one_const = pyo.Constraint(rule = rule_one)

    def rule_one(model):
        return (3*model.x1 + 10*model.x2 + 5*model.x3) <= 40
    model.rule_one_const = pyo.Constraint(rule = rule_one)

    def rule_one(model):
        return (3*model.x1 + 10*model.x2 + 5*model.x3) <= 40
    model.rule_one_const = pyo.Constraint(rule = rule_one)

    # solution
    result = pyo.SolverFactory("gurobi").solve(model, tee = True)

    print(f'The solver returned a status of: {result.solver.termination_condition}')

    if result.solver.termination_condition == pyo.TerminationCondition.optimal:
        print(pyo.TerminationCondition.optimal)
        print(f"Optimal value: {pyo.value(model.obj)}")
        print("Optimal solution:")
        print(f"  x1: {pyo.value(model.x1)}")
        print(f"  x2: {pyo.value(model.x2)}")    
        print(f"  x3: {pyo.value(model.x3)}")
              

main()