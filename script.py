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
    
    pd.DataFrame.from_dict(results).to_csv('results.csv', index=False)
    print('Data saved to results.csv')
    
    browser.close()