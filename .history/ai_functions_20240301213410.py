

def answer_question_llm(question, client):

    # Prepare the classification prompt with the classes from the CSV
    system_prompt = """
    Answer to the question in your own opinion.\n

    1 : if you agree\n 
    0 : if you are neutral\n
    -1 : if you do not agree\n

    Do not add any other text.\n
    """

    # Classify the GitHub project
    question_client = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    question_answer = question_client.choices[0].message.content

    print(question_answer)

    return question_answer