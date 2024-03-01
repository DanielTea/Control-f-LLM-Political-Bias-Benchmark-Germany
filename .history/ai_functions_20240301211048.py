

def create_a_blogpost_readme(question, client):

    # Prepare the classification prompt with the classes from the CSV
    system_prompt = """
    
    """

    # Classify the GitHub project
    question_client = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    question_answer = question_client.choices[0].message.content

    print(question_answer)

    return question_answer