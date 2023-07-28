import openai
from prompts.relevant_information_persona import get_relevant_information_persona 

def get_relevant_information(user_question: str):
    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": get_relevant_information_persona()
                    }, {
                        "role": "user",
                        "content": user_question
                        }
                    ]
                )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"

