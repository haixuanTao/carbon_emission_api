import requests
import csv
import os
import time

from flask_restful import Resource
from flask import current_app as app

ACCOUNT_JSON_INFO = "https://www.instagram.com/%s/?__a=1"
MEDIA_INFO_URL = (
    "https://i.instagram.com/api/v1/feed/user/%s/"
    "?exclude_comment=true&only_fetch_first_carousel_media=false"
)
TAGGED_MEDIA_INFO_URL = "https://i.instagram.com/api/v1/usertags/%s/feed/?"
HEADERS_PATH = "headers.csv"
HEADERS_STATIC_PATH = "headers.csv"


class Search(Resource):
    def __init__(self):
        with open(
            os.path.join(app.static_folder, HEADERS_PATH), mode="r"
        ) as infile:
            reader = csv.reader(infile)
            self.headers_params = {rows[0]: rows[1] for rows in reader}

    def get(self, user_id: int, is_verified: str) -> dict:
        """Get the media for a user. If the user is verified do not take the
        tagged media and go further in the media history.

        Args:
            user_id (int): The instagram user id
            is_verified (str): Boolean checking if the account is a verified
            account

        Returns:
            dict: The resulting json to be used in the ui.
        """
        # TODO: Do several pages
        # while not_enough_data and more_available:

        response_json = {"status": "ok", "items": []}

        if is_verified == "true":
            response_json["items"] += self.get_pictures_from_url(
                MEDIA_INFO_URL % user_id, 10
            )
        else:
            response_json["items"] += self.get_pictures_from_url(
                MEDIA_INFO_URL % user_id, 5
            )
            response_json["items"] += self.get_pictures_from_url(
                TAGGED_MEDIA_INFO_URL % user_id, 5
            )

        return response_json

    def get_pictures_from_url(self, url: str, number_of_pages: int) -> list:

        results = []

        current_page = 0
        more_available = True
        next_max_id = 0

        response_temporary = requests.get(
            url=url, headers=self.headers_params
        ).json()

        more_available = response_temporary["more_available"]
        current_page += 1

        results += response_temporary["items"]
        time.sleep(0.2)

        while current_page < number_of_pages and more_available:
            next_max_id = response_temporary["next_max_id"]

            response_temporary = requests.get(
                url=url + "&max_id=" + str(next_max_id),
                headers=self.headers_params,
            ).json()

            current_page += 1
            more_available = response_temporary["more_available"]
            results += response_temporary["items"]

            time.sleep(0.2)

        return results
