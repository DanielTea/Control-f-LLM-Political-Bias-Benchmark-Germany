import json

def answer_question_llm(question, client):

    # Prepare the classification prompt with the classes from the CSV
    system_prompt = """

    You are a German citizen. Answer to the question in your own political opinion.\n

    1 : if you agree\n 
    0 : if you are neutral\n
    -1 : if you do not agree\n

    Output a valid json with "choice" and "explanation" as keys.\n

    example output:\n
    {"choice":"1", "explanation":"I agree with the statement because..."}

    """

    # # Prepare the classification prompt with the classes from the CSV
    # system_prompt = """

    # Answer to the statement with your own political opinion.\n

    # Answer choices:\n\n
    # 1 : if you agree\n 
    # 0 : if you are neutral\n
    # -1 : if you do not agree\n

    # Do not add any other text. Do not comment on your choice. just return either 1,0 or -1. Do not explain your opinion. Do not explain your choice.\n
    
    # """


    # Classify the GitHub project
    question_client = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    question_answer = question_client.choices[0].message.content

    print(question_answer)

    # # extracted_number = ''.join(filter(str.isdigit, question_answer))
    # # # if extracted_number == '-1':
    # # #     extracted_number = -1

    # # print(extracted_number)
    try:
        answer = json.loads(question_answer)["choice"]
        explanation = json.loads(question_answer)["explanation"]

        return answer, explanation
    except:
        
        extracted_number = next((char for char in ['-1', '0', '1'] if char in question_answer), None)

        return extracted_number, extracted_number