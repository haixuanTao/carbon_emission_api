import requests
import csv
import os

from flask_restful import Resource
from flask import current_app as app

ACCOUNT_JSON_INFO = "https://www.instagram.com/%s/?__a=1"
MEDIA_INFO_URL = "https://i.instagram.com/api/v1/feed/user/%s/?exclude_comment=true&only_fetch_first_carousel_media=false"
TAGGED_MEDIA_INFO_URL = "https://i.instagram.com/api/v1/usertags/%s/feed/?"
HEADERS_PATH = "headers.csv"
HEADERS_STATIC_PATH = "headers.csv"


class Search(Resource):
    def get(self, user_id):

        with open(
            os.path.join(app.static_folder, HEADERS_PATH), mode="r"
        ) as infile:
            reader = csv.reader(infile)
            headers_params = {rows[0]: rows[1] for rows in reader}

        # TODO: Do several pages
        # while not_enough_data and more_available:
        response_own = requests.get(
            url=MEDIA_INFO_URL % user_id, headers=headers_params
        ).json()

        # TODO: Do several pages
        # Get tagged media
        response_tagged = requests.get(
            url=TAGGED_MEDIA_INFO_URL % user_id, headers=headers_params
        ).json()

        # group together
        response_own["items"] += response_tagged["items"]

        return response_own
