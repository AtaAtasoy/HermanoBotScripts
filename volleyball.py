from bs4 import BeautifulSoup
from flask import Blueprint, json
from werkzeug.exceptions import NotFound
import requests
import os

volleyball_module = Blueprint('volleyball', __name__)

@volleyball_module.route('/')
def volleyball():
    try:
        ticket_seller_url = os.getenv('VOLLEYBALL_TICKET_SELLER_URL')
        volleyball_matches_url = os.getenv('VOLLEYBALL_MATCHES_URL')
        webpage = requests.get(volleyball_matches_url)
        soup = BeautifulSoup(webpage.content, 'html.parser')
        results = soup.find("div", class_="resultsGrid")
        children = results.findAll("a", recursive=False)
        schedule = []

        for child in children:
            title = child.span.text
            location = child.p.text
            date = ''.join([i for i in child.find("p", class_="dates").text if i.isalnum() or i == "-"])
            
            result = {
                "title": title,
                "location": location,
                "date": date,
                "ticket_url": ticket_seller_url + child["href"]
            }

            schedule.append(result)

        response_data = json.dumps(schedule, ensure_ascii=False).encode("utf8")
        return response_data

    except Exception:
        return {"message": "Could not fetch ticket information", "status": "500"}