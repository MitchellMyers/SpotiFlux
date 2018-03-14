import spotipy
import credentials
from spotipy.oauth2 import SpotifyClientCredentials
import time
import os
from pygame import mixer
import pygame
import wget
from random import *
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication, QPushButton)
import sys


class SpotiPiGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.category = ""

        btn1 = QPushButton("Start", self)
        btn1.move(60, 90)
        btn1.clicked.connect(self.buttonClicked)

        combo = QComboBox(self)
        combo.addItem("")
        combo.addItem("decades")
        combo.addItem("pop")
        combo.addItem("hiphop")
        combo.addItem("jazz")

        combo.move(50, 50)

        combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('SpotiPi')
        self.show()

    def onActivated(self, text):
        self.category = text

    def buttonClicked(self):
        SpotiPiGUI.runSpotiPi(self)

    def runSpotiPi(self):

        client_credentials_manager = SpotifyClientCredentials(client_id=credentials.client_id,
                                                              client_secret=credentials.client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        playlistsCat = sp.category_playlists(category_id=self.category)
        totalTracks = []
        finalTracks = []
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
            filename = wget.download(songUrl)
            finalTracks.append((songName, filename))

        for songName, song in finalTracks:
            try:
                mixer.init(buffer=131072)
                mixer.music.load(song)
                time.sleep(3)
                print("\nNow playing... {}".format(songName))
                mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(300)
                os.remove(song.replace('.mp3', ''))
            except:
                continue
        sys.exit()


if __name__ == '__main__':
    app = QApplication([])
    ex = SpotiPiGUI()
    sys.exit(app.exec_())
