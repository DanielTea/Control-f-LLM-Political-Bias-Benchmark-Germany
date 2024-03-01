from playwright.sync_api import sync_playwright
import pandas as pd
import time

url = "https://www.wahl-o-mat.de/bundestagswahl2021/app/main_app.html"

def get_response():
    answers_map = {
        '-1': 2,
        '0' : 1,
        '1' : 0
    }
    
    while True:
        print('\nPlease input:\n1 : if you agree\n0 : if you are neutral\n-1 : if you do not agree')
        response = input()
        if response in ['-1', '0', '1']:
            return answers_map[response]
        
        print('\nWrong input.')

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    page.click("text=Start")
    
    for index, item in enumerate(page.locator('//*[@id="theses-slider"]/div[1]/ol/li').all()):
        question = item.locator('p >> nth=0').inner_text()
        print(f"\nQuestion {index + 1}: {question}")

        res = get_response()
        item.locator(f"li >> nth={res}").click()
        
        time.sleep(0.2)
    
    answers_map = {
        'Sie haben zugestimmt.': 'stimme zu',
        'Sie haben neutral gestimmt.' : 'neutral',
        'Sie haben nicht zugestimmt.' : 'stimme nicht zu'
    }
    
    results = []
    for item in page.locator('//*[@id="form_themen"]/div/ol/li').all():
        question = item.locator('//div[2]/div[1]/h2/button/span[2]').inner_text().strip()
        description = item.locator('//div[2]/div[2]').inner_text().strip()
        answer = item.locator('//div[2]/div[1]/h2/span/span/span[2]').inner_text().strip()
        
        result = {
            'question': question,
            'description': description,
            'answer': answers_map[answer]
        }
        results.append(result)
        
    pd.DataFrame.from_dict(results).to_csv('results.csv', index=False)
    print('Data saved to results.csv')

    browser.close()