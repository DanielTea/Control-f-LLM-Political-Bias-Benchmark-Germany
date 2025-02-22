from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
import random

import openai
from ai_functions import *


url = "https://www.wahl-o-mat.de/bundestagswahl2021/app/main_app.html"

# Read HEADLESS_MODE environment variable to determine headless state
headless_mode = os.getenv('HEADLESS_MODE', 'false') == 'true'

def get_response():
    answers_map = {
        '-1': 2,
        '0' : 1,
        '1' : 0
    }


    if os.getenv('RANDOM_ANSWERS', 'false') == 'true':
        return answers_map[random.choice([2, 1, 0])], None  # Randomly select among -1, 0, 1 mapped values
    
    if os.getenv('USE_LLM', 'false') == 'true':

        api_key = os.getenv('OPENAI_API_KEY')

        if os.getenv('USE_CLOSEDAI', 'false') == 'true':
            client = openai.OpenAI(api_key = "dummy", 
                                   base_url="http://localhost:1234/v1"
                                    # base_url ="http://localhost:4891/v1"
                                   )
            answer, explanation = answer_question_llm(question, client)
            return answers_map[answer], explanation
        else:
            api_key = os.getenv('OPENAI_API_KEY')
            client = openai.OpenAI(api_key = api_key)
            answer, explanation = answer_question_llm(question, client)
            return answers_map[answer], explanation

    
    while True:
        print('\nPlease input:\n1 : if you agree\n0 : if you are neutral\n-1 : if you do not agree')
        response = input()
        if response in ['-1', '0', '1']:
            return answers_map[response], None
        
        print('\nWrong input.')

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=headless_mode)
    page = browser.new_page()
    page.goto(url)

    page.click("text=Start")

    questions = []
    explanations = []
    
    for index, item in enumerate(page.locator('//*[@id="theses-slider"]/div[1]/ol/li').all()):
        question = item.locator('p >> nth=0').inner_text()
        print(f"\nQuestion {index + 1}: {question}")
        questions.append(question)
        
        res, exp = get_response()
        if exp:
            explanations.append(exp)
        else:
            explanations.append(res)

        item.locator(f"li >> nth={res}").click()


        
        time.sleep(0.2)
    
    page.click("text='weiter zur Auswahl der Parteien'")
    page.click("text='Hier können Sie alle Parteien gleichzeitig auswählen'")
    page.click("text='weiter zu Ihrem Wahl-O-Mat-Ergebnis'")  
    
    time.sleep(5)  
    page.screenshot(path="screenshot.png", full_page=True)
    print('Screenshot saved to screenshot.png')
    
    results = []
    for i, item in enumerate(page.locator('//*[@id="wommain"]/main/section/ol/li').all()):
        party = item.locator('xpath=h2/button/span[2]').inner_text().strip()
        description = item.locator('xpath=div[2]/div/div[1]/div[1]/p').inner_text().strip()
        percentage = item.locator('xpath=div[1]/p').inner_text().strip()      

        result = {
            'party': party,
            'description': description,
            'percentage': percentage
        }
        results.append(result)
    
    pd.DataFrame.from_dict(results).to_csv('parties_results.csv', index=False)
    print('Data saved to results.csv')

    data = {
        'Questions': questions,
        'Answers': explanations
    }

    pd.DataFrame.from_dict(data).to_csv('questions_answers.csv', index=False)
    print('Data saved to questions_answers.csv')
    
    browser.close()