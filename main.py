import openai

# chatgpt persona
from prompts.main_persona import get_assistent_profile
from utils.desired_value import get_desired_value 
from utils.extract_info import extract_info
from utils.question_relevant_information import get_relevant_information 

# OpenAi key
openai.api_key = "YOUR_API_KEY"

def answer_question(user_question: str):
    try:
        info = get_relevant_information(user_question)
        info_array = extract_info(info)
        desired_value = get_desired_value(info_array)

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
                        "content": f"This is the data you need: {desired_value}"
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

