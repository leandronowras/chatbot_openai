import re

def extract_info(input_str):
    company_pattern = r"Company: ([^.]+)"
    financial_term_pattern = r"Financial term: ([^.]+)"
    year_pattern = r"Year: (\d{4})"

    company_match = re.search(company_pattern, input_str)
    financial_term_match = re.search(financial_term_pattern, input_str)
    year_match = re.search(year_pattern, input_str)

    if company_match and financial_term_match and year_match:
        company = company_match.group(1).strip()
        financial_term = financial_term_match.group(1).strip()
        year = int(year_match.group(1))
        return [company, financial_term, year]
    else:
        return []

