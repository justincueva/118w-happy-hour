from flask import Flask, render_template

from src.scraper import HappyHourScraper
from src.extractor import HappyHourExtractor
import os

class HappyHourApp:
    def __init__(self, url):
        self.scraper = HappyHourScraper(url)
        self.extractor = HappyHourExtractor()
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
        self.app = Flask(__name__, template_folder=template_dir)

        @self.app.route("/")
        def home():
            page_text = self.scraper.scrape_page()
            happy_hour_info = self.extractor.extract_happy_hour(page_text) if page_text else "Happy Hour info not available"
            return render_template("template.html", happy_hour=happy_hour_info)

    def run(self):
        self.app.run(debug=True)

