from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
class HappyHourScraper:

    def __init__(self, url):
        self.url = url
    def scrape_page(self):
        options = Options()
        options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        page_text = None

        try:
            driver.get(self.url)
            time.sleep(3)
            page_text = driver.find_element(By.TAG_NAME, "body").text

        except Exception as e:
            print(f"Error Scraping Page: {e}")

        finally:
            driver.quit()
            return page_text




