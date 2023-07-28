import pandas as pd

# load data
balance_sheet_statement = pd.read_csv("./data/US_INDU_BALANCE_SHEET_STATEMENT.csv")
calculations = pd.read_csv("./data/US_INDU_CALCULATIONS.csv")
cash_flow_statement = pd.read_csv("./data/US_INDU_CASH_FLOW_STATEMENT.csv")
cash_income_statement = pd.read_csv("./data/US_INDU_INCOME_STATEMENT.csv")

# desired columns
def get_fiscal_year_columns():
    return ['name', 'fiscal_period', 'fiscal_year']

def get_cash_income_statement_columns():
    return ['name', 'totalrevenue', 'fiscal_year', 'netincome']

def get_calculations_columns():
    return ['name', 'pricetoearnings', 'fiscal_year', 'dividendyield', 'roe']

# get columns
def get_companies_fiscal_year(fiscal_period = "FY"):
    return balance_sheet_statement.loc[balance_sheet_statement["fiscal_period"] == fiscal_period, get_fiscal_year_columns()]

def get_companies_total_revenue_and_cash_income(fiscal_period = "FY"):
    return cash_income_statement.loc[cash_income_statement["fiscal_period"] == fiscal_period, get_cash_income_statement_columns()]

def get_companies_price_to_ear_dividend_yield_and_roe(fiscal_period = "FY"):
    return calculations.loc[calculations["fiscal_period"] == fiscal_period, get_calculations_columns()] 

# get full desired data set
def get_full_data_set():
    all_companies_data = pd.merge(get_companies_fiscal_year(), get_companies_total_revenue_and_cash_income())
    return pd.merge(all_companies_data, get_companies_price_to_ear_dividend_yield_and_roe())
