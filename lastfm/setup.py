#---------------------------------------------------------------------------------------------------
# Author: Will Fenton
# Date:   May 21 2019
# Updated April 22 2020 for the webapp project


# This sets up the project structure (makes directories, etc.)
# Gets a Last.fm api key from the user
# Generates a config file, and validates existing config files
#---------------------------------------------------------------------------------------------------

import os
import sys
import sqlite3
from configparser import ConfigParser, ExtendedInterpolation
from api_key import get_api_key, validate_api_key
from db_functions import validate_username


def setup():
    # check whether database exists, if so ask whether to delete
    if os.path.exists("database.sqlite3"):
        user_input = input("Database already exists. Delete? (y/n) ").lower()
        while user_input not in ("y", "n"):
            user_input = input("Database already exists. Delete? (y/n) ").lower()
        if user_input == "y":
            os.remove("database.sqlite3")
    
    # create database
    if not os.path.exists("database.sqlite3"):
        db = sqlite3.connect("database.sqlite3")

        # Create table
        db.execute(f"CREATE TABLE scrobbles (unix_timestamp INTEGER, text_timestamp TEXT, artist_name TEXT, artist_mbid TEXT, track_name TEXT, track_mbid TEXT, album_name TEXT, album_mbid TEXT, last_fm_url TEXT, small_image_url TEXT, medium_image_url TEXT, large_image_url TEXT, extralarge_image_url TEXT, PRIMARY KEY (track_name, artist_name, album_name, unix_timestamp));")

        db.commit()
        db.close()

    config_parser = ConfigParser(interpolation=ExtendedInterpolation())

    if os.path.exists("config.ini"):

        user_input = input("Config already exists. Delete? (y/n) ").lower()
        while user_input not in ("y", "n"):
            user_input = input("Config already exists. Delete? (y/n) ").lower()
        if user_input == "y":
            os.remove("config.ini")
        else:
            config_parser.read("config.ini")

            # validate api key
            api_key = config_parser.get("settings", "api_key")
            assert(validate_api_key(api_key))

            # validate username
            username = config_parser.get("settings", "username")
            assert(validate_username(username, api_key))

    # create config
    if not os.path.exists("config.ini"):
        api_key = get_api_key()

        username = input("Last.fm username: ").lower()
        while not validate_username(username, api_key):
            username = input("Last.fm username: ").lower()

        config_parser["settings"] = {
            "api_key": api_key,
            "username": username
        }

        with open("config.ini", 'w') as f:
            config_parser.write(f)
            

if __name__ == "__main__":
    setup()