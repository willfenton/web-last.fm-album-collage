import sqlite3
import json

def main():

    albums = {
        "albums": []
    }

    db = sqlite3.connect("database.sqlite3")
    results = db.execute("SELECT album_name, artist_name, extralarge_image_url, MIN(unix_timestamp), MAX(unix_timestamp), COUNT(*) FROM scrobbles GROUP BY album_name, artist_name HAVING COUNT(DISTINCT track_mbid) > 1 ORDER BY COUNT(*) DESC LIMIT 200;").fetchall()
    for result in results:
        album_name, artist_name, image_url, min_timestamp, max_timestamp, num_scrobbles = result
        print(album_name, artist_name, num_scrobbles)
        album = {
            "album_name": album_name,
            "artist_name": artist_name,
            "image_url": image_url,
            "min_timestamp": min_timestamp,
            "max_timestamp": max_timestamp,
            "num_scrobbles": num_scrobbles
        }
        albums["albums"].append(album)
    
    with open("albums.json", "w") as f:
        f.write(json.dumps(albums))

    db.close()

if __name__ == "__main__":
    main()