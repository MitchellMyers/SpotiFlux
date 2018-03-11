import spotipy
import credentials
from spotipy.oauth2 import SpotifyClientCredentials
import time
import os
from pygame import mixer
import pygame
import wget
from random import *

sentimentDict = {'sad' : ['sadness', 'lonely', 'alone', 'by myself', 'sad']}


client_credentials_manager = SpotifyClientCredentials(client_id=credentials.client_id,
                                                      client_secret=credentials.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlistsCat = sp.category_playlists(category_id="hiphop")
totalTracks = []
playlists = playlistsCat['playlists']['items']
i = 0
while (len(totalTracks) < 11) and i < len(playlists):
    playlist = playlists[i]
    playId = playlist['id']
    playOb = sp.user_playlist('spotify', playId)
    index = randint(0, len(playOb['tracks']['items']) - 1)
    trackId = playOb['tracks']['items'][index]['track']['id']
    trackOb = sp.track(trackId)
    if trackOb['preview_url']:
        previewUrl = trackOb['preview_url'] + '.mp3'
        if len(previewUrl.rsplit('.', 1)) == 2 and (trackOb['name'], previewUrl) not in totalTracks:
            totalTracks.append((trackOb['name'], previewUrl))
    shuffle(totalTracks)

for songName, songUrl in totalTracks:
    print("\nNow playing... {}".format(songName))
    try:
        filename = wget.download(songUrl)
        mixer.init(buffer=131072)
        mixer.music.load(filename)
        time.sleep(3)
        mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(300)
        os.remove(filename.replace('.mp3', ''))
    except:
        continue

