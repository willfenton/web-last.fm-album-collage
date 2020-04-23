#---------------------------------------------------------------------------------------------------
# Author: Will Fenton
# Date:   July 14 2019
# Updated April 22 2020 for the webapp project

# Database utility functions
#---------------------------------------------------------------------------------------------------

import re
import os
import sys
import sqlite3
import requests
from shutil import rmtree, copyfileobj
from datetime import datetime
from configparser import ConfigParser, ExtendedInterpolation


# returns the config parser object
def get_config():
    config_parser = ConfigParser(interpolation=ExtendedInterpolation())
    config_parser.read("config.ini")
    return config_parser


# validate last.fm username
def validate_username(username, api_key):
    username = username.lower()
    match = re.match(r"^[a-zA-Z][a-zA-Z0-9\-_]{1,14}$", username)
    if match is None:
        return False
    api_url = f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={api_key}&format=json"
    response = requests.get(api_url)
    return response.status_code == 200


# call the last.fm api and download a page of 200 scrobbles
def get_page(username, api_key, page_number):
    api_url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={api_key}&format=json&page={page_number}&limit=200"
    page = requests.get(api_url)
    return page.json()


# get the number of pages of scrobbles (200 scrobbles / page) for a given user
def get_num_pages(username, api_key):
    page = get_page(username, api_key, 1)
    attributes = page["recenttracks"]["@attr"]
    print("{} scrobbles total ({} pages)".format(attributes["total"], attributes["totalPages"]))
    return int(attributes["totalPages"])


# insert a page of scrobbles into the database
def insert_page(db, username, page):
    insert_string = f"INSERT INTO scrobbles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    try:
        tracks = page["recenttracks"]["track"]
        for track in tracks:
            try:
                unix_timestamp = track["date"]["uts"]
                text_timestamp = track["date"]["#text"]

                artist_name = track["artist"]["#text"]
                artist_mbid = track["artist"]["mbid"]

                track_name = track["name"]
                track_mbid = track["mbid"]

                album_name = track["album"]["#text"]
                album_mbid = track["album"]["mbid"]

                last_fm_url = track["url"]

                small_image_url = track["image"][0]["#text"]
                medium_image_url = track["image"][1]["#text"]
                large_image_url = track["image"][2]["#text"]
                extralarge_image_url = track["image"][3]["#text"]

                # print(f"{track_name} by {artist_name}")

                arguments = [unix_timestamp, text_timestamp, artist_name, artist_mbid, track_name, track_mbid, album_name, album_mbid, last_fm_url, small_image_url, medium_image_url, large_image_url, extralarge_image_url]
                db.execute(insert_string, arguments)
                
            # Either the track is currently playing or scrobble is in the database already
            except Exception as e:
                # print(e)
                pass

    except Exception as e:
        print(e)


# download all new scrobbles for a given user since the last time they were updated
# downloads all scrobbles if it's the first time
def update_data(db, username, api_key):
    username = username.lower()
    try:
        last_update_timestamp = int(db.execute(f"SELECT unix_timestamp FROM scrobbles ORDER BY unix_timestamp DESC LIMIT 1;").fetchone()[0])
        readable = datetime.utcfromtimestamp(last_update_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Last updated {readable}. Now updating.")        
    except:
        last_update_timestamp = 0
        print("Downloading all data.")

    config_parser = get_config()

    num_pages = get_num_pages(username, api_key)

    # Download all pages with new scrobbles
    for i in range(1, num_pages + 1):
        print(f"Page {i} of {num_pages}")

        page = get_page(username, api_key, i)

        try:
            first_timestamp = int(page["recenttracks"]["track"][0]["date"]["uts"])
            last_timestamp = int(page["recenttracks"]["track"][len(page["recenttracks"]["track"]) - 1]["date"]["uts"])
        except:
            first_timestamp = int(datetime.now().strftime("%s"))
            last_timestamp = int(datetime.now().strftime("%s"))

        if first_timestamp < last_update_timestamp:
            break
        if last_timestamp < last_update_timestamp:
            insert_page(db, username, page)
            break
        insert_page(db, username, page)

    new_scrobbles = db.execute(f"SELECT track_name, album_name, artist_name FROM scrobbles WHERE unix_timestamp > ? ORDER BY unix_timestamp ASC;", [last_update_timestamp]).fetchall()
    count = len(new_scrobbles)
    for scrobble in new_scrobbles:
        track_name, album_name, artist_name = scrobble
        print(f"{track_name} by {artist_name}")
    print(f"Downloaded {count} new scrobbles.")

    db.commit()
    db.close()
