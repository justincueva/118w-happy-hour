from flask import Flask, render_template
from src.data import happy_hour_schedule
from src.main import update_happy_hour_data

app = Flask(__name__)

@app.before_request
def run_scraper():
    #here we could include a data base where we can pull uploaded urls from
    url = "https://thetablesj.com/happy-hour/"
    update_happy_hour_data(url)


@app.route("/")
def home():
    return render_template("template.html", happy_hour=happy_hour_schedule)

if __name__ == "__main__":
    app.run(debug=True)
