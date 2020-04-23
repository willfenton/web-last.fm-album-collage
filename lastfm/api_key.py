#---------------------------------------------------------------------------------------------------
# Author: Will Fenton
# Date:   May 21 2019

# Functions for validating and getting Last.fm api keys
#---------------------------------------------------------------------------------------------------

import requests

#---------------------------------------------------------------------------------------------------

# takes a last.fm api key as a string and returns true if it's a valid key, false if it's invalid
def validate_api_key(api_key):
    api_url = f"https://ws.audioscrobbler.com/2.0/?method=chart.gettoptags&limit=1&api_key={api_key}&format=json"
    response = requests.get(api_url)
    json = response.json()
    return "error" not in json

# gets, validates and returns last.fm API key
def get_api_key():
    api_key = input("Enter your last.fm API key: ")
    while not validate_api_key(api_key):
        print("Invalid API key")
        api_key = input("Enter your last.fm API key: ")
    return api_key

#---------------------------------------------------------------------------------------------------
