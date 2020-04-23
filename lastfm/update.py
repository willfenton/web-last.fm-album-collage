import sqlite3
from db_functions import get_config, update_data

if __name__ == "__main__":
    config_parser = get_config()
    api_key = config_parser.get("settings", "api_key")
    username = config_parser.get("settings", "username")
    db = sqlite3.connect("database.sqlite3")
    update_data(db, username, api_key)