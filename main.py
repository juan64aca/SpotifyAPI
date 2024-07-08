import pandas as pd
import requests
import json
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv

from utils.auth import Token
from utils.spotify import Spotify, Track, Playlist, Album, Artist, User

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

token = Token(client_id, client_secret)

spotify = Spotify(token)

user_id = 1289334468

user_playlists = spotify.get_user_playlists(user_id)
print(user_playlists)