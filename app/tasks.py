from apscheduler.schedulers.background import BackgroundScheduler
from .db_manager import get_all_restaurants, update_restaurant_info
from .scraper import HappyHourScraper
from .extractor import HappyHourExtractor
import atexit

scheduler = BackgroundScheduler()

def re_scrape_all():
    restaurants = get_all_restaurants()
    for r in restaurants:
        try:
            scraper = HappyHourScraper(r['url'])
            raw = scraper.scrape_page()
            info = HappyHourExtractor.extract_happy_hour(raw)
            update_restaurant_info(r['id'], raw, info['weekdays'], info['weekends'])
        except Exception as e:
            print(f"Error re-scraping {r['url']}: {e}")

def init_scheduler(app):
    scheduler.add_job(func=re_scrape_all, trigger='cron', hour=3)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())