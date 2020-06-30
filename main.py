import psycopg2
import spotipy
import spotipy.util as util

username = '114923525'
scope = 'user-library-read user-top-read user-read-currently-playing user-read-recently-played'
token = util.prompt_for_user_token(username, scope, client_id='a5d677b7f92647b69ab65752478588d4',
                                   client_secret='07c5a3ddf0c745ca9a80b8a5ceb07dc0', redirect_uri='http://localhost/')

if token:
    print("Connecting to database...")
    conn = psycopg2.connect(database="postgres", user="updater", password="updater", host="scott")
    print("Connected to database")

    cur = conn.cursor()

    sp = spotipy.client.Spotify(auth=token)
    results = sp.current_user_recently_played(limit=50)
    items = results['items']
    print("Received {} tracks.".format(len(items)))
    for item in items:
        played_at = item['played_at']

        track = item['track']
        track_id = track['id']
        track_name = track['name']
        track_duration_ms = track['duration_ms']

        artist = track['artists'][0]
        artist_id = artist['id']
        artist_name = artist['name']

        album = track['album']
        album_id = album['id']
        album_name = album['name']

        cur.execute("""INSERT INTO plays (username, played_at, track_id, track_name, track_duration_ms, artist_id,
            artist_name, album_id, album_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                    (username, played_at, track_id, track_name, track_duration_ms, artist_id, artist_name, album_id,
                     album_name))
        if cur.rowcount > 0:
            print("Inserted {} - {}.".format(track_name, artist_name))

    conn.commit()
    print("Update finished.")

else:
    print("No token for", username)
