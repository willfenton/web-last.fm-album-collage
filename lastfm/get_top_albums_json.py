import sqlite3
import json

def main():

    albums = {
        "albums": []
    }

    db = sqlite3.connect("database.sqlite3")
    top_albums = db.execute("SELECT album_name, artist_name, extralarge_image_url, MIN(unix_timestamp), MAX(unix_timestamp), COUNT(*) FROM scrobbles GROUP BY album_name, artist_name HAVING COUNT(DISTINCT track_mbid) > 1 ORDER BY COUNT(*) DESC LIMIT 200;").fetchall()
    for top_album in top_albums:
        album_name, artist_name, image_url, min_timestamp, max_timestamp, num_scrobbles = top_album
        print(album_name, artist_name, num_scrobbles)
        album = {
            "album_name": album_name,
            "artist_name": artist_name,
            "image_url": image_url,
            "min_timestamp": min_timestamp,
            "max_timestamp": max_timestamp,
            "num_scrobbles": num_scrobbles
        }

        top_tracks = db.execute("SELECT track_name, COUNT(*) FROM scrobbles WHERE album_name=? AND artist_name=? GROUP BY track_name ORDER BY COUNT(*) DESC;", [album_name, artist_name]).fetchall()
        album["top_track"] = top_tracks[0][0]
        
        albums["albums"].append(album)
    
    with open("albums.json", "w") as f:
        f.write(json.dumps(albums))

    db.close()

if __name__ == "__main__":
    main()