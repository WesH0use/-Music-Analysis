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


def check_for_valid_data(df: pd.DataFrame) -> bool:
    # Check to see if the dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    # Check for primary keys (timestamps)
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Primary key check is violated.")

    # Check for null values
    if df.isnull().values.any():
        raise Exception("Null values found")

    # Check that all timestamps are from yesterday
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
            raise Exception("At least one of the songs does not come from previous 24 hours.")

    return True

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

    song_title = []
    artist = []
    time_played_list = []
    timestamps = []

    for song in data['items']:
        song_title.append(song["track"]["name"])
        artist.append(song["track"]["album"]["artists"][0]["name"])
        time_played_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])


    song_dict = {
        "song_title" : song_title,
        "artists": artist,
        "played_at": time_played_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_title", "artists", "played_at", "timestamp"])

    # Validate
    if check_for_valid_data(song_df):
      print("Data is valid, please proceed to loadstage")







