from data_set import get_full_data_set

def get_desired_value(array_data):
    company_name = array_data[0] # possivel bug: se uma empresa tiver parcialmente o nome da outra (apple market) 
    financial_data = array_data[1]
    desired_year = array_data[2]
    dataset = get_full_data_set()

    row = dataset.loc[
        (dataset["name"].str.contains(company_name, case=False)) &
        (dataset["fiscal_year"] == desired_year)
    ]
    return row[financial_data].iat[0]


