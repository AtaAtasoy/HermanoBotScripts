from http import HTTPStatus
import json
import os
import tweepy
from flask import Blueprint, request
from dotenv import load_dotenv
import jsonpickle

twitter_module = Blueprint('twitter', __name__)
load_dotenv()

@twitter_module.route('/')
def performTwitterSearch():
    query_string = request.args.get('query')
    if not query_string:
        return json.dump({
            "message": "did not receive parameter 'query'",
            "status": HTTPStatus.BAD_REQUEST
        })

    max_results = request.args.get('maxResults') if request.args.get(
        'maxResults') is not None else 10
    sort_order = request.args.get('sortOrder') if request.args.get(
        'sortOrder') is not None else 'recency'

    client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))
    tweets = client.search_recent_tweets(
        query=query_string,
        max_results=max_results,
        sort_order=sort_order,
        expansions=['author_id', 'referenced_tweets.id'])

    response = jsonpickle.encode(tweets.data)

    return response
