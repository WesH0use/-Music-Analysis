#!/usr/bin/env python

import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3


DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "wes.house" # your Spotify username
TOKEN = "BQBlqk2oPljOqA3Dkb-dJmOknLDkKy52bqhZWUsQ4uVXuV2V2a4aKoD0rRN30wG04PYyxm_XkHYNiHvn6dDkkWbaR_fRSR9qFhAG-4hptY-eak16RfuOlxifR2VGA2ehKsUg61-3RvvKDSQFmrU" # your Spotify API token


if __name__ == "__main__":


    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    data = r.json()

    print(data)
