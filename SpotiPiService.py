import spotipy
import credentials
from spotipy.oauth2 import SpotifyClientCredentials
import time


client_credentials_manager = SpotifyClientCredentials(client_id=credentials.client_id,
                                                      client_secret=credentials.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        time.sleep(3)
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None