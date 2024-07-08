import requests


class Playlist:
    def __init__(self, data):
        self.data = data
        self.id = None
        self.name = None
        self.description = None
        self.owner = None
        self.public = None
        self.tracks = None
        self.build()

    def build(self):
        self.id = self.data['id']
        self.name = self.data['name']
        self.description = self.data['description']
        self.owner = self.data['owner']
        self.public = self.data['public']
        tracks = self.data['tracks']['items']
        self.tracks = [Track(track['track']) for track in tracks]

        return True


class User:
    def __init__(self, data):
        self.data = data
        self.id = None
        self.name = None
        self.build()

    def build(self):
        self.id = self.data['id']
        self.name = self.data['display_name']

        return True


class Artist:
    def __init__(self, data):
        self.data = data
        self.id = None
        self.name = None
        self.build()

    def build(self):
        self.id = self.data['id']
        self.name = self.data['name']

        return True


class Album:
    def __init__(self, data):
        self.data = data
        self.id = None
        self.name = None
        self.type = None
        self.artists = None
        self.release = None
        self.total_tracks = None
        self.build()

    def build(self):
        try:
            self.id = self.data['id']
            self.name = self.data['name']
            self.type = self.data['album_type']
            self.artists = [Artist(artist) for artist in self.data['artists']]
            self.release = self.data['release_date']
            self.total_tracks = self.data['total_tracks']

            return True

        except:
            print("Can't build album.")


class Track:
    def __init__(self, data):
        self.data = data
        self.id = None
        self.name = None
        self.artists = None
        self.album = None
        self.duration = None
        self.explicit = None
        self.popularity = None

        self.build()

    def build(self):
        self.id = self.data['id']
        self.name = self.data['name']
        self.artists = [Artist(artist) for artist in self.data['artists']]
        self.album = Album(self.data['album'])
        self.duration = self.data['duration_ms']
        self.explicit = self.data['explicit']
        self.popularity = self.data['popularity']

        return True


class Spotify:
    def __init__(self, auth):
        self.url = "https://api.spotify.com/v1"
        self.token = auth
        self.headers = {
            'Authorization': f'Bearer {self.token.token}'
        }

    def get_user_playlists(self, user_id):
        endpoint = self.url + f'/users/{user_id}/playlists'
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            playlists = response.json()
            playlists = playlists['items']
            playlists_ids = [playlist['id'] for playlist in playlists]
            playlists = [self.get_playlist(playlist_id) for playlist_id in playlists_ids]

            return playlists

        else:
            print(f"Failed to retrieve playlists: {response.status_code} - {response.text}")

    def get_playlist(self, playlist_id):
        endpoint = self.url + f'/playlists/{playlist_id}'
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            playlist = response.json()

            return Playlist(playlist)

        else:
            print(f"Failed to retrieve playlists: {response.status_code} - {response.text}")
