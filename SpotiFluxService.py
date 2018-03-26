import time
import os
from pygame import mixer
import pygame
import wget
from random import choice, shuffle
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication, QPushButton)
from SpotifyExtClient import SpotifyCategoryPlaylistsQuery, SpotifyPlaylistTracksQuery
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
        combo.addItem("hiphop")
        combo.addItem("pop")
        combo.addItem("decades")
        combo.addItem("jazz")
        combo.addItem("toplists")
        combo.addItem("mood")
        combo.addItem("workout")
        combo.addItem("chill")
        combo.addItem("edm_dance")
        combo.addItem("focus")
        combo.addItem("rock")
        combo.addItem("party")
        combo.addItem("country")
        combo.addItem("sleep")
        combo.addItem("latin")
        combo.addItem("rnb")
        combo.addItem("romance")
        combo.addItem("indie_alt")
        combo.addItem("jazz")
        combo.addItem("gaming")
        combo.addItem("classical")
        combo.addItem("reggae")
        combo.addItem("metal")
        combo.addItem("soul")
        combo.addItem("blues")
        combo.addItem("funk")
        combo.addItem("punk")
        combo.addItem("popculture")
        combo.addItem("kids")
        combo.addItem("kpop")

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

        spotifyPlayCatClient = SpotifyCategoryPlaylistsQuery()
        spotifyPlayClient = SpotifyPlaylistTracksQuery()

        playlistsCat = spotifyPlayCatClient.get(category_id=self.category, country='US', limit=50, offset=0)
        totalTracks = []
        finalTracks = []

        for playlistId in playlistsCat:
            trackDict = spotifyPlayClient.get(playlist_id=playlistId, limit=100, offset=0)
            trackPrevUrl, trackName = choice(list(trackDict.items()))
            trackPrevUrl += '.mp3'
            if len(trackPrevUrl.rsplit('.', 1)) == 2 and (trackPrevUrl, trackName) not in totalTracks:
                totalTracks.append((trackPrevUrl, trackName))
            if len(totalTracks) > 15:
                break
        shuffle(totalTracks)
        for songUrl, songName in totalTracks:
            filename = wget.download(songUrl)
            finalTracks.append((filename, songName))

        for songUrl, songName in finalTracks:
            try:
                mixer.init()
                mixer.music.load(songUrl)
                print("\nNow playing... {}".format(songName))
                mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(31000)
                mixer.quit()
                os.remove(songUrl.replace('.mp3', ''))
                time.sleep(5)
            except:
                continue
        sys.exit()


if __name__ == '__main__':
    app = QApplication([])
    ex = SpotiPiGUI()
    sys.exit(app.exec_())
