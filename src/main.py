from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI

import time
import os

from src.data import update_happy_hour
# Set up OpenAI API Key

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

# Sets up selenium to extract all content from page, has exception
# to catch url loading errors
def scrape_happy_hour_page(url):
    options = Options()
    options.add_argument('--headless')
    service=Service(ChromeDriverManager().install())
    driver=webdriver.Chrome(service=service,options=options)
    page_text = None

    try:
        driver.get(url)
        time.sleep(3)
        page_text = driver.find_element(By.TAG_NAME, "body").text

    except Exception as e:
        print(f"Error Scraping Page: {e}")

    finally:
        driver.quit()
        return page_text

# Takes text file from the scraper to feed into chatgpt to get the
# happy hour schedule
def extract_happy_hour(page_text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Extract only the Happy Hour schedule from the following restaurant webpage text."},
            {"role": "user", "content": page_text}
        ]
    )
    return response.choices[0].message.content

#updates display template in html located in templates/template
def update_happy_hour_data(url):
    page_text = scrape_happy_hour_page(url)
    happy_hour_text = extract_happy_hour(page_text)

    new_schedule = {
        "weekdays": "Not Available",
        "weekends": "Not Available"
    }

    if "Mon" in happy_hour_text or "Tue" in happy_hour_text or "Wed" in happy_hour_text:
        new_schedule["weekdays"] = happy_hour_text

    if "Sat" in happy_hour_text or "Sun" in happy_hour_text:
        new_schedule["weekends"] = happy_hour_text

    update_happy_hour(new_schedule)
    print("✅ Happy Hour data updated successfully!")


