import base64

from flask_restful import Resource
import requests
import credentials


class SpotifyAuthorizationQuery(Resource):

    def get(self):
        auth_header = base64.b64encode(str(credentials.client_id + ':' + credentials.client_secret).encode())
        headers = {'Authorization': 'Basic {}'.format(auth_header.decode())}
        payload = {'grant_type': 'client_credentials',
                   'response_type': 'token'}
        url = "https://accounts.spotify.com/api/token"
        jsonData = requests.post(url=url, headers=headers, data=payload)
        try:
            auth_token = jsonData.json()['access_token']
            return auth_token
        except KeyError:
            return None


class SpotifyCategoryPlaylistsQuery(Resource):

    def get(self, category_id, country, limit, offset):
        spotifyAuthClient = SpotifyAuthorizationQuery()
        auth_token = spotifyAuthClient.get()
        playlist_ids = []
        if auth_token is not None:
            headers = {'Authorization': 'Bearer {}'.format(auth_token)}
            query_params = {'country': country,
                            'limit': limit,
                            'offset': offset}
            url = "https://api.spotify.com/v1/browse/categories/{}/playlists".format(category_id)
            jsonData = requests.get(url=url, headers=headers, params=query_params)
            try:
                spotify_playlists = jsonData.json()['playlists']
                for playlist in spotify_playlists['items']:
                    playlist_ids.append(playlist['id'])
                return playlist_ids
            except KeyError:
                return []
        else:
            return []

class SpotifyPlaylistTracksQuery(Resource):

    def get(self, playlist_id, limit, offset):
        spotifyAuthClient = SpotifyAuthorizationQuery()
        auth_token = spotifyAuthClient.get()
        headers = {'Authorization': 'Bearer {}'.format(auth_token)}
        query_params = {'limit': limit,
                        'offset': offset}
        url = "https://api.spotify.com/v1/users/spotify/playlists/{}/tracks".format(playlist_id)
        jsonData = requests.get(url=url, headers=headers, params=query_params)
        trackDict = {}
        try:
            tracks = jsonData.json()['items']
            for track in tracks:
                track = track['track']
                track_url = track['preview_url']
                track_name = track['name']
                if track_url and track_name:
                    trackDict[track['preview_url']] = track['name']
            return trackDict
        except KeyError:
            return {}
