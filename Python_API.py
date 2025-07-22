from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Fanshawe Scraper API is running"

@app.route('/programs')
def get_programs():
    base_url = "https://www.fanshawec.ca/programs-and-courses?page={}"
    headers = {"User-Agent": "Mozilla/5.0"}
    all_data = []

    for page in range(2):  # Keep this low during testing; increase to 26 for full scrape
        url = base_url.format(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        programs = soup.select("div.program--inner-wrapper")

        for prog in programs:
            try:
                anchor = prog.select_one(".program--title-wrapper a")
                name = anchor.select_one("span").get_text(strip=True)
                program_url = "https://www.fanshawec.ca" + anchor['href']
                credential = prog.select_one(".field--name-field-program-type .field__item").get_text(strip=True)
                location = prog.select_one(".field--name-field-campus-code .field__item").get_text(strip=True)

                all_data.append({
                    "name": name,
                    "credential": credential,
                    "location": location,
                    "url": program_url
                })
            except AttributeError:
                continue

    return jsonify(all_data)
