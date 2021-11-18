from os import abort
from bs4 import BeautifulSoup
from flask import Blueprint
from flask.json import jsonify
from werkzeug.exceptions import NotFound
import requests
import os

volleyball_module = Blueprint('volleyball', __name__)

@volleyball_module.route('/')
def volleyball():
    try:
        ticket_seller_url = os.getenv('VOLLEYBALL_TICKET_SELLER_URL')
        volleyball_games_url = os.getenv('VOLLEYBALL_GAMES_URL')
        webpage = requests.get(volleyball_games_url)
        soup = BeautifulSoup(webpage.content, 'html.parser')
        results = soup.find("div", class_="resultsGrid")
        children = results.findAll("a", recursive=False)
        schedule = []

        for child in children:
            title = ''.join([i for i in child.span.text if i.isalnum() or i == "-" or i == "(" or i == ")"])
            location = ''.join([i for i in child.span.text if i.isalnum() or i == "-" or i == "(" or i == ")"])
            date = ''.join([i for i in child.find("p", class_="dates").text if i.isalnum() or i == "-"])
            
            result = {
                "title": title,
                "location": location,
                "date": date,
                "ticket_url": ticket_seller_url + child["href"]
            }

            schedule.append(result)            
        return jsonify(schedule, 200)

    except NotFound:
        print("Not Found")
        abort(404)