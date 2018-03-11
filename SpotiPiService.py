import spotipy
import credentials
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util
import time
import itertools
import sys
from pygame import mixer
import wget

sentimentDict = {'sad' : ['sadness', 'lonely', 'alone', 'by myself', 'sad']}


client_credentials_manager = SpotifyClientCredentials(client_id=credentials.client_id,
                                                      client_secret=credentials.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# tracks = sp.search(q='sadness', type='track')
playlistsCat = sp.category_playlists(category_id="party")
totalTracks = []
while len(totalTracks) < 10:
    for i, playlist in enumerate(playlistsCat['playlists']['items']):
        playId = playlist['id']
        playOb = sp.user_playlist('spotify', playId)
        # totalTracks.append(trackOb['tracks'][0]['name'])
        trackId = playOb['tracks']['items'][0]['track']['id']
        trackOb = sp.track(trackId)
        previewUrl = trackOb['preview_url']

        filename = wget.download(previewUrl)
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()

        # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))

        # time.sleep(3)
    # if tracks['next']:
    #     playlists = sp.next(playlists)
    # else:
    #     playlists = None


# lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
#
# spotify = spotipy.Spotify()
# results = spotify.artist_top_tracks(lz_uri)
#
# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", username)
