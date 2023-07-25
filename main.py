import openai
import pandas as pd
import re

# OpenAi key
# openai.api_key = "YOUR-API-KEY"

# load data
balance_sheet_statement = pd.read_csv("./chatbot-task/data/US_INDU_BALANCE_SHEET_STATEMENT.csv")
calculations = pd.read_csv("./chatbot-task/data/US_INDU_CALCULATIONS.csv")
cash_flow_statement = pd.read_csv("./chatbot-task/data/US_INDU_CASH_FLOW_STATEMENT.csv")
cash_income_statement = pd.read_csv("./chatbot-task/data/US_INDU_INCOME_STATEMENT.csv")

# chatgpt persona
def get_assistent_profile():
    return  '''You are an economist with extensive knowledge of finance, you only give brief answers and you always have the data you need. Your style of answer is the following: Question: How much did walmart generate in sales in 2021?

Answer: In 2021, Walmart Inc generated $XXX billion in sales.
Note: Corresponding information is Total Revenue
Question: What was the bottom line for walgreens common shareholders in 2022?

Answer: The bottom line for Walgreens Boots Alliance Inc's common shareholders in 2022 was $XXX million.
Note: Corresponding information is Net Income / (Loss) Attributable to Common Shareholders
Question: How much was verizon stock worth compared to its earnings in 2021?

Answer: In 2021, for every dollar of earnings, Verizon Communications Inc's stock was worth XX.XX.
Note: Corresponding information is Price to Earnings (P/E)
Question: What percentage of its share price did Visa return to its shareholders as dividends in 2022?

Answer: In 2022, Visa Inc returned X.XX% of its share price to its shareholders as dividends.
Note: Corresponding information is Dividend Yield
Question: What was the efficiency of Apple in generating profits from its shareholders' equity in 2021?

Answer: In 2021, Apple Inc generated a return of XX.XX% on its shareholders' equity.
Note: Corresponding information is Return on Equity (ROE)
'''


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

# main chatbot function
def answer_question(user_question: str) -> str:
    regex_year = r"\b\d{4}\b"
    match = re.search(regex_year, user_question)
    input_year = match.group()
    data_set = get_full_data_set()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": get_assistent_profile()
                }, {
                "role": "user",
                "content": user_question
                }, {
                    "role": "assistant",
                    "content": f"Here are all the data you need in csv: {data_set.loc[data_set['fiscal_year'] == int(input_year)].to_csv()}"
                    }
                  ]
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"

#  Examples
def run_examples():
    question = "How much did walmart generate in sales in 2021?"
    answer = answer_question(question)
    print(answer)

    question = "What was the bottom line for walgreens common shareholders in 2022?"
    answer = answer_question(question)
    print(answer)

    question = "How much was verizon stock worth compared to its earnings in 2021?"
    answer = answer_question(question)
    print(answer)

    question = "What percentage of its share price did Visa return to its shareholders as dividends in 2022?"
    answer = answer_question(question)
    print(answer)

    question = "What was the efficiency of Apple in generating profits from its shareholders' equity in 2021?"
    answer = answer_question(question)
    print(answer)

run_examples()
